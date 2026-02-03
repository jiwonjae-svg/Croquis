"""
Secure Key Management Module
Provides dynamic encryption key generation based on user-specific information
"""

import hashlib
import base64
import platform
import uuid
import os
from pathlib import Path
from cryptography.fernet import Fernet
from typing import Optional
import json
import zlib


class KeyManager:
    """
    Manages encryption keys using machine-specific information.
    Generates keys based on:
    - Machine UUID (hardware-based identifier)
    - OS username
    - Application-specific salt
    
    This ensures each installation has a unique key while maintaining
    deterministic key generation for the same user/machine.
    """
    
    _instance = None
    _key = None
    
    def __new__(cls):
        """Singleton pattern to ensure consistent key across application"""
        if cls._instance is None:
            cls._instance = super(KeyManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._key is None:
            self._key = self._generate_key()
    
    def _get_machine_id(self) -> str:
        """
        Get unique machine identifier.
        Uses multiple fallback methods for reliability.
        """
        try:
            # Method 1: Try to get hardware UUID (most reliable)
            machine_uuid = uuid.getnode()
            if machine_uuid:
                return str(machine_uuid)
        except Exception:
            pass
        
        try:
            # Method 2: Platform-specific machine ID
            if platform.system() == "Windows":
                # Windows: Use MachineGuid from registry
                import winreg
                try:
                    key = winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE,
                        r"SOFTWARE\Microsoft\Cryptography",
                        0,
                        winreg.KEY_READ | winreg.KEY_WOW64_64KEY
                    )
                    machine_guid, _ = winreg.QueryValueEx(key, "MachineGuid")
                    winreg.CloseKey(key)
                    if machine_guid:
                        return machine_guid
                except Exception:
                    pass
            elif platform.system() == "Darwin":  # macOS
                import subprocess
                result = subprocess.run(
                    ['ioreg', '-rd1', '-c', 'IOPlatformExpertDevice'],
                    capture_output=True,
                    text=True
                )
                # Parse IOPlatformUUID from output
                for line in result.stdout.split('\n'):
                    if 'IOPlatformUUID' in line:
                        return line.split('"')[-2]
            elif platform.system() == "Linux":
                # Linux: Try /etc/machine-id
                machine_id_file = Path("/etc/machine-id")
                if machine_id_file.exists():
                    return machine_id_file.read_text().strip()
        except Exception:
            pass
        
        # Method 3: Fallback to hostname + username combination
        return f"{platform.node()}-{os.getlogin()}"
    
    def _get_user_info(self) -> str:
        """Get current OS username"""
        try:
            return os.getlogin()
        except Exception:
            try:
                return os.environ.get('USERNAME') or os.environ.get('USER', 'default_user')
            except Exception:
                return 'default_user'
    
    def _generate_key(self) -> bytes:
        """
        Generate encryption key from machine-specific information.
        
        Key derivation process:
        1. Collect machine ID + username + application salt
        2. Hash with SHA-256
        3. Encode for Fernet compatibility
        
        Returns:
            bytes: Fernet-compatible encryption key
        """
        # Collect unique identifiers
        machine_id = self._get_machine_id()
        user_info = self._get_user_info()
        app_salt = "croquis_app_v2_secure"  # Application-specific salt
        
        # Combine identifiers
        key_material = f"{machine_id}:{user_info}:{app_salt}".encode('utf-8')
        
        # Generate key through SHA-256 hashing
        hash_digest = hashlib.sha256(key_material).digest()
        
        # Encode for Fernet (requires base64 URL-safe encoding)
        fernet_key = base64.urlsafe_b64encode(hash_digest)
        
        return fernet_key
    
    def get_key(self) -> bytes:
        """
        Get the encryption key.
        
        Returns:
            bytes: Fernet-compatible encryption key
        """
        return self._key
    
    def get_fernet(self) -> Fernet:
        """
        Get a Fernet cipher instance with the current key.
        
        Returns:
            Fernet: Ready-to-use Fernet cipher
        """
        return Fernet(self._key)
    
    def encrypt_data(self, data: dict) -> bytes:
        """
        Encrypt and compress dictionary data.
        
        Args:
            data: Dictionary to encrypt
            
        Returns:
            bytes: Encrypted data
        """
        fernet = self.get_fernet()
        json_str = json.dumps(data, ensure_ascii=False)
        # Compress with zlib (level 9 = max compression)
        compressed = zlib.compress(json_str.encode(), level=9)
        encrypted = fernet.encrypt(compressed)
        return encrypted
    
    def decrypt_data(self, encrypted: bytes) -> dict:
        """
        Decrypt and decompress data.
        
        Args:
            encrypted: Encrypted bytes
            
        Returns:
            dict: Decrypted dictionary
        """
        fernet = self.get_fernet()
        decrypted = fernet.decrypt(encrypted)
        # Decompress
        decompressed = zlib.decompress(decrypted)
        data = json.loads(decompressed.decode())
        return data
    
    def get_key_info(self) -> dict:
        """
        Get information about the current key (for debugging/logging).
        Does NOT expose the actual key.
        
        Returns:
            dict: Key metadata
        """
        machine_id = self._get_machine_id()
        user_info = self._get_user_info()
        
        # Create a hash of the key for verification (not the key itself)
        key_hash = hashlib.sha256(self._key).hexdigest()[:16]
        
        return {
            "machine_id_hash": hashlib.sha256(machine_id.encode()).hexdigest()[:16],
            "user": user_info,
            "key_fingerprint": key_hash,
            "platform": platform.system(),
            "python_version": platform.python_version()
        }


# Convenience functions for backward compatibility
_key_manager_instance: Optional[KeyManager] = None


def get_key_manager() -> KeyManager:
    """Get the global KeyManager instance (singleton)"""
    global _key_manager_instance
    if _key_manager_instance is None:
        _key_manager_instance = KeyManager()
    return _key_manager_instance


def encrypt_data(data: dict) -> bytes:
    """Convenience function: Encrypt data using the global key manager"""
    return get_key_manager().encrypt_data(data)


def decrypt_data(encrypted: bytes) -> dict:
    """Convenience function: Decrypt data using the global key manager"""
    return get_key_manager().decrypt_data(encrypted)


# Initialize on import
get_key_manager()
