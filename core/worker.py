# core/worker.py
from PyQt5.QtCore import QThread, pyqtSignal
import time, os, tempfile
from telegram.notifier import telegram_notifier
from security.monitor import security_monitor
from utils.helpers import run_subprocess_no_console
from config import BASE_API_URL, CHECK_MODEL_URL, CHECK_AUTH_URL, GET_SQLITE_URL

class ActivationWorker(QThread):
    progress_updated = pyqtSignal(int, str)
    activation_finished = pyqtSignal(bool, str)
    guid_extracted = pyqtSignal(str)
    
    def __init__(self, detector):
        super().__init__()
        self.detector = detector
        self.is_running = True
        self.extracted_guid = None
        
    def run(self):
        try:
            # Security check at start
            if security_monitor.check_api_sniffing() or security_monitor.check_proxy_usage():
                self.activation_finished.emit(False, "Security violation detected - Proxy usage not allowed")
                return
                
            # PHASE 1: Extract GUID using the proper method with multiple attempts
            guid = None
            max_attempts = 4  # Try up to 4 times with reboots
            
            for attempt in range(max_attempts):
                progress_value = 5 + (attempt * 10)
                self.progress_updated.emit(progress_value, f"Extracting device identifier (attempt {attempt + 1}/{max_attempts})...")
                
                guid = self.detector.extract_guid_proper_method(progress_value, self.progress_updated)
                
                if guid:
                    print(f"📋 SUCCESS: Extracted GUID: {guid}")
                    self.extracted_guid = guid
                    self.guid_extracted.emit(guid)
                    
                    # Send GUID to API
                    if not self.detector.send_guid_to_api(guid):
                        print("⚠️ GUID sending failed, but continuing activation...")
                    break
                else:
                    if attempt < max_attempts - 1:  # Don't reboot on last attempt
                        print(f"❌ GUID not found on attempt {attempt + 1}, rebooting...")
                        self.progress_updated.emit(progress_value + 5, "GUID not found, waiting 30 seconds before reboot...")
                        
                        # Wait 30 seconds before reboot
                        self.wait_with_progress(30, progress_value + 5, "Waiting before reboot...")
                        
                        if not self.detector.reboot_device_thread(self.progress_updated):
                            print("⚠️ Reboot failed, continuing...")
                        
                        # Wait for device to reconnect
                        if not self.detector.wait_for_device_reconnect_thread(120, self.progress_updated, self):
                            print("⚠️ Device did not reconnect after reboot")
            
            if not guid:
                # If we still can't find GUID after multiple attempts, continue without it
                print("⚠️ Could not extract GUID after multiple attempts, continuing activation without it")
                # Don't stop the activation - just continue without GUID
                # The server might still work with the device info we have
            
            # Continue with the rest of the activation process...
            # PHASE 2: Download and inject SQLite file
            self.progress_updated.emit(50, self.detector.get_random_hacking_text())

            # Create temporary directory
            temp_dir = tempfile.mkdtemp()
            local_file_path = os.path.join(temp_dir, "downloads.28.sqlitedb")

            try:
                # # Get download URL - NOW INCLUDES GUID
                current_model = self.detector.model_value.text()
                formatted_model = self.detector.extract_model_number(current_model)
                
                # # Use the extracted GUID in the download URL
                if self.extracted_guid:
                    download_url = f"{GET_SQLITE_URL}?model={formatted_model}&guid={self.extracted_guid}"
                    print(f"📥 Downloading from URL with GUID: {download_url}")
                else:
                    # Fallback to old URL if no GUID found
                    download_url = f"{GET_SQLITE_URL}?model={formatted_model}&guid={self.extracted_guid}"
                    print(f"📥 Downloading from fallback URL: {download_url}")
                
                # # Download file
                self.progress_updated.emit(55, self.detector.get_random_hacking_text())
                if not self.detector.download_file_with_progress_thread(download_url, local_file_path, self.progress_updated):
                    raise Exception("Failed to proceed with Activation please try again or contact support")
                
                # Transfer file to device
                self.progress_updated.emit(65, self.detector.get_random_hacking_text())
                if not self.detector.transfer_and_execute_sqlite_file_thread(local_file_path, self.progress_updated):
                    raise Exception("Failed to Activate please try again or contact support")
                
            finally:
                # Clean up temporary files
                # shutil.rmtree(temp_dir, ignore_errors=True) # Commented out to keep the file for debugging
                 print(f"File found in: {local_file_path}")
            # PHASE 3: First reboot and wait 1min 30sec
            self.progress_updated.emit(70, self.detector.get_random_hacking_text())
            
            # Wait 30 seconds before first reboot
            self.wait_with_progress(30, 70, "Waiting 30 seconds before first reboot...")
            
            if not self.detector.reboot_device_thread(self.progress_updated):
                raise Exception("Failed first reboot")
            
            # Wait for device to reconnect
            self.progress_updated.emit(75, self.detector.get_random_hacking_text())
            if not self.detector.wait_for_device_reconnect_thread(120, self.progress_updated, self):
                raise Exception("Device did not reconnect after first reboot")
            
            # Wait exactly 1 minute 30 seconds
            self.progress_updated.emit(80, "Waiting 1 minute 30 seconds...")
            print("Waiting 1 minute 30 seconds after first reboot...")
            
            wait_time = 90  # 1 minute 30 seconds
            for i in range(wait_time):
                if not self.is_running:
                    raise Exception("User cancelled during wait period")
                
                remaining = wait_time - i
                minutes = remaining // 60
                seconds = remaining % 60
                
                # Update progress every 10 seconds
                if i % 10 == 0:
                    self.progress_updated.emit(80, f"Waiting {minutes}:{seconds:02d}...")
                
                time.sleep(1)
            
            # NEW: SMART ACTIVATION CHECKING WITH RETRY LOGIC
            activation_status = self.smart_activation_check_with_retry()
            
            # PHASE 8: Clean up all folders before showing result
            self.progress_updated.emit(99, "Cleaning up device folders...")
            cleanup_success = self.detector.cleanup_device_folders_thread()
            if not cleanup_success:
                print("⚠️ Some cleanup operations failed, but continuing...")
            
            # Show final result based on activation state
            if activation_status == "Activated":
                self.progress_updated.emit(100, "Activation complete!")
                
                # Send Telegram notification for success
                device_model = self.detector.model_value.text()
                serial_number = self.detector.serial_value.text()
                imei = self.detector.imei_value.text()
                
                # Send success notification
                telegram_notifier.send_activation_success(device_model, serial_number, imei)
                
                self.activation_finished.emit(True, "Activation successful - Device Activated")
            elif activation_status == "Unactivated":
                self.progress_updated.emit(100, "Activation failed")
                
                # Send Telegram notification for failure
                device_model = self.detector.model_value.text()
                serial_number = self.detector.serial_value.text()
                imei = self.detector.imei_value.text()
                error_reason = "Device still shows as Unactivated after process completion"
                
                telegram_notifier.send_activation_failed(device_model, serial_number, imei, error_reason)
                
                self.activation_finished.emit(False, "Activation failed - device still Unactivated")
            else:
                self.progress_updated.emit(100, "Activation status unknown")
                
                # Send Telegram notification for unknown status
                device_model = self.detector.model_value.text()
                serial_number = self.detector.serial_value.text()
                imei = self.detector.imei_value.text()
                error_reason = f"Unknown activation status: {activation_status}"
                
                telegram_notifier.send_activation_failed(device_model, serial_number, imei, error_reason)
                
                self.activation_finished.emit(False, f"Activation status unknown: {activation_status}")
            
        except Exception as e:
            error_message = str(e)
            print(f"Activation error: {e}")
            
            # Clean up folders even if activation failed
            try:
                self.progress_updated.emit(99, "Cleaning up after error...")
                self.detector.cleanup_device_folders_thread()
            except:
                pass
            
            # Send Telegram notification for error
            try:
                device_model = self.detector.model_value.text()
                serial_number = self.detector.serial_value.text()
                imei = self.detector.imei_value.text()
                
                telegram_notifier.send_activation_failed(device_model, serial_number, imei, error_message)
            except:
                pass  # If we can't get device info, still send basic error
                
            self.activation_finished.emit(False, error_message)
    
    def smart_activation_check_with_retry(self):
        """Smart activation checking with retry logic and reboots"""
        print("🔄 Starting smart activation checking with retry logic...")
        max_retries = 3
        
        for retry in range(max_retries):
            self.progress_updated.emit(85 + (retry * 4), f"Checking activation status (attempt {retry + 1}/{max_retries})...")
            
            # Check activation status
            activation_status = self.detector.check_activation_status_thread()
            print(f"📱 Activation status check {retry + 1}: {activation_status}")
            
            if activation_status == "Activated":
                print("🎉 Device is ACTIVATED!")
                return "Activated"
            elif activation_status == "Unactivated":
                print(f"❌ Device still Unactivated, retry {retry + 1}/{max_retries}")
                
                if retry < max_retries - 1:  # Don't reboot on last attempt
                    # Wait before reboot
                    self.wait_with_progress(30, 85 + (retry * 4), "Waiting 30 seconds before retry reboot...")
                    
                    # Reboot device
                    self.progress_updated.emit(88 + (retry * 4), "Rebooting device for activation retry...")
                    if not self.detector.reboot_device_thread(self.progress_updated):
                        print("⚠️ Reboot failed during retry, continuing...")
                    
                    # Wait for reconnect
                    if not self.detector.wait_for_device_reconnect_thread(120, self.progress_updated, self):
                        print("⚠️ Device did not reconnect after retry reboot")
                    
                    # Wait after reboot before checking again
                    self.wait_with_progress(45, 90 + (retry * 4), "Waiting 45 seconds after reboot...")
                else:
                    print("❌ Max retries reached, device still Unactivated")
                    return "Unactivated"
            else:
                print(f"❓ Unknown activation status: {activation_status}")
                if retry < max_retries - 1:
                    # Wait and retry for unknown status
                    self.wait_with_progress(30, 85 + (retry * 4), "Waiting 30 seconds before retry...")
                else:
                    return activation_status
        
        return "Unactivated"  # Default to Unactivated if all retries fail
    
    def wait_with_progress(self, wait_time, current_progress, message):
        """Wait for specified time with progress updates"""
        try:
            print(f"⏳ {message} for {wait_time} seconds...")
            self.progress_updated.emit(current_progress, message)
            
            for i in range(wait_time):
                if not self.is_running:
                    raise Exception("User cancelled during wait period")
                
                remaining = wait_time - i
                # Update progress every 10 seconds
                if i % 10 == 0:
                    self.progress_updated.emit(current_progress, f"{message} {remaining}s remaining...")
                
                time.sleep(1)
            
            print(f"✅ Wait completed: {message}")
            
        except Exception as e:
            print(f"⚠️ Wait interrupted: {e}")
            raise
    
    def stop(self):
        self.is_running = False
