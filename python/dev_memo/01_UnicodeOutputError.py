# import io,sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import io,sys

text = "한글日本語"
print(sys.stdout.encoding)
try:
    print(text)
except Exception as ex:
    print(ex)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
print(sys.stdout.encoding)
print(text)