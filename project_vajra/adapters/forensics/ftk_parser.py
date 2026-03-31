"""
FTK Forensic Evidence Parser
"""
import os
import sys
from typing import Dict, Any

class FTKParser:
    """Parse FTK disk images using pytsk3"""
    
    def __init__(self):
        self._pytsk3 = None
        self._pyewf = None
        self._load_libraries()
    
    def _load_libraries(self):
        """Conditionally load pytsk3 and pyewf (Linux only)"""
        if sys.platform == "linux":
            try:
                import pytsk3
                import pyewf
                self._pytsk3 = pytsk3
                self._pyewf = pyewf
            except ImportError:
                pass
    
    def parse_image(self, image_path: str) -> Dict[str, Any]:
        """Parse FTK image file into structured evidence"""
        # Fallback for Windows/macOS development environments
        if self._pytsk3 is None:
            return self._get_mock_image()
            
        pytsk3 = self._pytsk3
        pyewf = self._pyewf
        
        # Handle EWF format (common in FTK exports)
        if image_path.lower().endswith(('.e01', '.ewf')):
            filenames = pyewf.glob(image_path)
            ewf_handle = pyewf.handle()
            ewf_handle.open(filenames)
            img_info = pytsk3.Img_Info(ewf_handle)
        else:
            img_info = pytsk3.Img_Info(image_path)
            
        # Get filesystem info
        fs_info = pytsk3.FS_Info(img_info)
        
        # Extract filesystem metadata with safe attribute access
        fs_data = {
            "type": str(getattr(fs_info.info, 'ftype', 'unknown')),
            "block_size": getattr(fs_info.info, 'block_size', 0),
            "block_count": getattr(fs_info.info, 'block_count', 0),
            "root_inode": getattr(fs_info.info, 'root_inum', 0)
        }
        
        # Extract files
        files = []
        try:
            root_dir = fs_info.open_dir(inode=fs_info.info.root_inum)
            for entry in root_dir:
                if entry.info.name.name not in [b".", b".."]:
                    files.append(self._extract_file_info(entry, pytsk3))
        except Exception:
            pass  # Handle permission errors gracefully
                
        return {
            "image_info": {
                "path": image_path,
                "size": os.path.getsize(image_path) if os.path.exists(image_path) else 0
            },
            "filesystem": fs_data,
            "files": files
        }
    
    def _extract_file_info(self, entry, pytsk3) -> Dict[str, Any]:
        """Extract metadata for a single file"""
        try:
            name = entry.info.name.name
            if isinstance(name, bytes):
                name = name.decode('utf-8', 'ignore')
        except Exception:
            name = "unknown"
            
        return {
            "name": name,
            "size": getattr(entry.info.meta, 'size', 0) if hasattr(entry.info, 'meta') else 0,
            "type": "dir" if hasattr(entry.info.meta, 'type') and entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR else "file",
            "created": getattr(entry.info.meta, 'crtime', 0) if hasattr(entry.info, 'meta') else 0,
            "modified": getattr(entry.info.meta, 'mtime', 0) if hasattr(entry.info, 'meta') else 0,
            "inode": getattr(entry.info, 'addr', 0)
        }
    
    def _get_mock_image(self) -> Dict[str, Any]:
        """Return a simulated disk image for testing and cross-platform dev."""
        from project_vajra.logging_config import logger
        logger.warning("pytsk3 not available. Using simulated FTK image data.")
        return {
            "image_info": {"path": "simulated.E01", "size": 1024000},
            "filesystem": {"type": "NTFS", "block_size": 4096, "block_count": 250, "root_inode": 5},
            "files": [
                {"name": "wallet.dat", "size": 256, "type": "file", "created": 1672531200, "modified": 1672531200, "inode": 10},
                {"name": "Documents", "size": 4096, "type": "dir", "created": 1672531200, "modified": 1672531200, "inode": 11}
            ]
        }