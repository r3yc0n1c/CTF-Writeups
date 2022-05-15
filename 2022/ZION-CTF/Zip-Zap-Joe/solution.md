```bash
❯ 7z e gs-15-vs.zip
```
```bash
❯ mkdir files
```
```bash
❯ find . -type f -exec mv {} ./files \;
```

```bash
❯ ulimit -n 2048
```

```py
import os
from PIL import Image

images = [Image.open(os.path.join('./files/', '%s.png' % i)) for i in range(1, 1024)]
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (1024, 1024))

x_offset = 0
y_offset = 0
count = 1
for im in images:
    if(count%32 == 0):
        y_offset += im.size[0]
        x_offset = 0
    new_im.paste(im, (x_offset, y_offset))
    x_offset += im.size[0]
    count += 1

new_im.save('./output.png')
new_im.show()
```

```bash
❯ zbarimg output.png
QR-Code:zionctf{We1C0m3_t0_7H3_Z1On_C7F_Obl4di0B14Da}
scanned 1 barcode symbols from 1 images in 0.08 seconds
```

```
so the Flag is : zionctf{We1C0m3_t0_7H3_Z1On_C7F_Obl4di0B14Da}
```
