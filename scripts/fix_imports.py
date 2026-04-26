#!/usr/bin/env python3
"""Fix import issues in backend files."""

import os
import re

def fix_imports_in_file(filepath):
    """Fix import statements in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    content = original_content
    
    # Fix imports from api.dependencies
    content = re.sub(r'from api\.dependencies\.', r'from backend.api.dependencies.', content)
    
    # Fix imports from services.
    content = re.sub(r'from services\.', r'from backend.services.', content)
    
    # Fix imports from core.
    content = re.sub(r'from core\.', r'from backend.core.', content)
    
    # Fix imports from models.
    content = re.sub(r'from models\.', r'from backend.models.', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return content != original_content

def main():
    """Main function to fix imports."""
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    # Files to fix
    files_to_fix = [
        'api/routes/batches.py',
        'api/routes/certificates.py',
        'api/routes/compliance.py',
        'api/routes/delegation.py',
        'api/routes/reports.py',
        'api/routes/telemetry.py',
        'core/compliance.py',
        'services/certificate_service.py',
        'services/batch_service.py',
        'services/qrcode_service.py',
        'services/delegation_service.py',
        'services/report_service.py',
        'blockchain/minting.py',
        'blockchain/verification.py',
        'blockchain/web3_client.py',
    ]
    
    fixed_count = 0
    for file_rel in files_to_fix:
        filepath = os.path.join(backend_dir, file_rel)
        if os.path.exists(filepath):
            try:
                if fix_imports_in_file(filepath):
                    print(f"Fixed imports in {file_rel}")
                    fixed_count += 1
                else:
                    print(f"No changes needed in {file_rel}")
            except Exception as e:
                print(f"Error fixing {file_rel}: {e}")
        else:
            print(f"File not found: {file_rel}")
    
    print(f"\nFixed imports in {fixed_count} files.")

if __name__ == '__main__':
    main()