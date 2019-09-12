# shamfinder

Shamfinder is a framework that detects homograph IDN.



## Homograph DB

Homograph DB is a part of shamfinder.

This is used when comparing the reference domain with the target domain.

This database is consist of two files (**simchar.json** and **confusables_v12-1_in_draft.json**).



### simchar.json

- how to create

1. multi_psnr.py

   Generate images(50*50 pixels) with embeddded character.

   Then I compare them brute force and calculate psnr by multi proccess.

   

2. json_summaraize.py

   This file adds the meta infomation and generates a json file.  The meta information is shown below.

    

   - black_point ... the number of pixels whose RGB is (255, 255, 255)

   - codepoint ... codepoint is the number which represent single character

   - demical ... codepoint(demical)

   - lang ... the name of the block to which the character belongs (<http://www.unicode.org/Public/UNIDATA/Blocks.txt>)

   - name ...character name decided by Unicode Consortium

   - similar_char ... list of characters similar to original character (psnr >= 23.7)

   - psnr ... PSNR(Peak signal-to-noise ratio) is a rate indicating how similar the images are (<https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio>) 

     

3. remove_less_10pixles.py

   This file removes charactes with less than 10 pixels whose RGB is (255, 255, 255) from json file.



As a result of executing these, the following file is obtained.

- example

```
"i": {
        "black_point": 15,
        "codepoint": "U+0069",
        "demical": 105,
        "lang": "Basic Latin",
        "name": "LATIN SMALL LETTER I",
        "similar_char": [
            {
                "black_point": 19,
                "char": "ɨ",
                "codepoint": "U+0268",
                "demical": 616,
                "lang": "IPA Extensions",
                "name": "LATIN SMALL LETTER I WITH STROKE",
                "psnr": 27.96
            },
            
            			:
            			:
            			:
            			:
```







### confusable_v12-1_in_draft.json

This file shows characters that are similar to lowercase letters and characters that are similar to numbers based on the confusables.txt provided by the Unicode Consortium. And it is made based on the following conditions.

1. These characters are allowed to use IDNA by **IDNA2008 and Unicode 12.0.0** (<https://tools.ietf.org/id/draft-faltstrom-unicode12-00.html>)
2. These characters have fonts in **unifont** (<http://unifoundry.com/unifont/index.html>)



- example

```
"b": [
        {
            "block": "Unified Canadian Aboriginal Syllabics",
            "char": "ᑲ",
            "demical": 5234,
            "name": "CANADIAN SYLLABICS KA"
        },
        {
            "block": "Unified Canadian Aboriginal Syllabics",
            "char": "ᖯ",
            "demical": 5551,
            "name": "CANADIAN SYLLABICS AIVILIK B"
        },
        
        					:
        					:
        					:
```

