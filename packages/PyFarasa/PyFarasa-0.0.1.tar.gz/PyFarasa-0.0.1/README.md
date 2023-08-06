# Farasa Segmenter (Non-official)

## Usage
```python
>>> from farasa import segmentation as s
>>> s.segmentLine("والمكتبات")
>>> ['و+ال+مكتب+ات']
>>> segments = s.segmentLine(" ثورة في مشهد الكعك")
>>> for tok in segments:
>>> ... print(tok)
>>> ...
>>> 'ثور+ة'
>>> 'في'
>>> 'مشهد'
>>> 'ال+كعك'
```




