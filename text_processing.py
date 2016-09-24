
def xor(a1,a2):
   if a1 and (not a2):
       return True
   if a2 and (not a1):
       return True
   return False


def words_split(txt):
   space_symbols = [' ','\n',',',';','.','?','!',':','(',')']
   seg_l=[]
   seg='' 
   for i in range(0,len(txt)):
      seg = seg+txt[i]
      if (i+1 == len(txt)) or xor((txt[i] in space_symbols), (txt[i+1] in space_symbols)): 
        if txt[i] in space_symbols:
             seg_type = 'space'
        else:
             seg_type = 'word' 
        seg_l.append({'content':seg,'type': seg_type}) 
        seg = ''

   #txtmap = [ ch in space_symbols for ch in txt ]

   return seg_l

def output_fragment (fragment_id, split_text):
  st=''
  for token in split_text:
     if token['type']=='word':
       st=st+'<span class="word" id="%sw%s">%s</span>' % (fragment_id, token["word_id"],token["content"])
     else: 
       st=st+token["content"] 
  return st

def words_numbering (split_text):
  i=1
  for token in split_text:
    if token['type']=='word':
      token["word_id"]=i
      i=i+1
  return split_text


