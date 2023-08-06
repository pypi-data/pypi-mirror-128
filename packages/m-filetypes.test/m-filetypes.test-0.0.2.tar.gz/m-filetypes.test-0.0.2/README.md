##  Thư viện kiểm tra file type.

### Cài đặt:

```bash
 $ pip3 install m-filetypes
 ```

### Sử dụng
```python
from mobio.libs.filetypes.file import File
from mobio.libs.filetypes.common import ExtensionImage

File.check_filetype_by_file_extensions(
    file_binary=file, # Check filetype của định dạng file binary.Mặc định None
    file_path=file_path, # Check filetype của path file
    extensions=[ExtensionImage.PNG] # Danh sách extension cần check.
)

```

#### Lấy extensions support
- Extension Image:
```python
from mobio.libs.filetypes.common import ExtensionImage
ExtensionImage.LIST_EXTENSION_SUPPORTED
```
- Extension Document:
```python
from mobio.libs.filetypes.common import ExtensionDocument
ExtensionDocument.LIST_EXTENSION_SUPPORTED
```
- Extension Document:
```python
from mobio.libs.filetypes.common import ExtensionAudio
ExtensionAudio.LIST_EXTENSION_SUPPORTED
```