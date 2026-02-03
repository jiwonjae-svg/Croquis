"""
Core Module
Contains business logic: encryption, key management, data processing
"""

from .key_manager import KeyManager, get_key_manager, encrypt_data, decrypt_data

__all__ = ['KeyManager', 'get_key_manager', 'encrypt_data', 'decrypt_data']
