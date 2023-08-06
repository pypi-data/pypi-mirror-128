try:
    import upsidedown  
    
except (ModuleNotFoundError, ImportError):
    pass

try:
    from zalgo_text import zalgo as zalg
    
except (ModuleNotFoundError, ImportError):
    pass

try:
    from nltk import pos_tag, word_tokenize
    
except (ModuleNotFoundError, ImportError):
    pass

try:
    import base65536
    
except (ModuleNotFoundError, ImportError):
    pass

import random

from .exception import *
from .objtype import objtype

gen = random.SystemRandom()

class text:
    """Text manipulation garbage"""
    def __init__(self):
        try:
            self.zal = zalg.zalgo()
            
        except NameError:
            pass
        
    def _objrepl(self, str_, a, b):
        """Function dependency of rouxls()"""
        out = str(str_).replace(a.lower(), b.lower())
        out = str(out).replace(a.title(), b.title())
        out = str(out).replace(a.upper(), b.upper())
        return out
    
    def _objreplic(self, str_, a, b):
        out = str(str_).replace(a.lower(), b)
        out = str(out).replace(a.title(), b)
        out = str(out).replace(a.upper(), b)
        return out
    
    def _swap(self, arr, i_1 ,i_2):
        temp = arr[i_1]
        arr[i_1] = arr[i_2]
        arr[i_2] = temp
        return arr
        
    def udown(self, intexta):
        """Generates upside-down text"""
        try:
            return upsidedown.transform(str(intexta))
        
        except NameError:
            raise ModuleError("Upsidedown must be installed. Try pip install upsidedown or pip install beetroot[text].")
        
    def zalgo(self, intexta, **kwargs):
        """Generates Zalgo text"""
        craziness = float(
            kwargs.get(
                "crazy",
                1
            )
        )
        try:
            self.zal.numAccentsUp = (round(craziness), round(craziness * 10))
            self.zal.numAccentsDown = (round(craziness), round(craziness * 10))
            self.zal.numAccentsMiddle = (round(craziness), round(craziness * 10))
            self.zal.maxAccentsPerLetter = round(craziness * 40)
            return self.zal.zalgofy(str(intexta))
        
        except NameError:
            raise ModuleError("Zalgo_texta must be installed. Try pip install zalgo-texta or pip install beetroot[text].")
        
    def rouxls(self, sentence):
        """Makeseth thou soundeth likest Rouxls, Thy Duke of Puzzles."""
        try:
            yee = pos_tag(word_tokenize(sentence))
            
            out = []
            for i in range(0, len(yee)):
                if yee[i][1].startswith("NN") or yee[i][1].startswith("VB"):
                    dumb = random.randint(1, 100)
                    if dumb <= 40:
                        if yee[i][0].endswith("a") or yee[i][0].endswith("e") or yee[i][0].endswith("i") or yee[i][0].endswith("o") or yee[i][0].endswith("u"):
                            out.append("".join([str(yee[i][0]), "th"]))
                            
                        elif yee[i][0].endswith("s"):
                            if yee[i][0].endswith("es"):
                                out.append("".join([str(yee[i][0]), "t"]))
                                
                            else:
                                out.append("".join([str(yee[i][0]), "e"]))
                            
                        elif yee[i][0].endswith("y"):
                            out.append("".join([str(yee[i][0])[:-1], "ie"]))
                            
                        else:
                            out.append("".join([str(yee[i][0]), "eth"]))
                        
                    elif dumb > 40 and dumb <= 80:
                        if yee[i][0].endswith("a") or yee[i][0].endswith("e") or yee[i][0].endswith("i") or yee[i][0].endswith("o") or yee[i][0].endswith("u"):
                            out.append("".join([str(yee[i][0]), "st"]))
                            
                        elif yee[i][0].endswith("s"):
                            if yee[i][0].endswith("es"):
                                out.append("".join([str(yee[i][0]), "t"]))
                                
                            else:
                                out.append("".join([str(yee[i][0]), "e"]))
                            
                        elif yee[i][0].endswith("y"):
                            out.append("".join([str(yee[i][0])[:-1], "ie"]))
                            
                        else:
                            out.append("".join([str(yee[i][0]), "est"]))

                    elif dumb > 80 and dumb <= 90:
                        if yee[i][1].startswith("NN"):
                            if yee[i][0].endswith("e"):
                                out.append(str(yee[i][0]))
                                
                            else:
                                out.append("".join([str(yee[i][0]), "e"]))
                            
                        else:
                            if yee[i][0].endswith("a") or yee[i][0].endswith("e") or yee[i][0].endswith("i") or yee[i][0].endswith("o") or yee[i][0].endswith("u"):
                                out.append("".join([str(yee[i][0]), "t"]))
                                
                            elif yee[i][0].endswith("s"):
                                if yee[i][0].endswith("es"):
                                    out.append("".join([str(yee[i][0]), "st"]))
                                
                                else:
                                    out.append("".join([str(yee[i][0]), "e"]))
                                
                            elif yee[i][0].endswith("y"):
                                out.append("".join([str(yee[i][0])[:-1], "ie"]))
                                
                            else:
                                out.append("".join([str(yee[i][0]), "est"]))

                    else:
                        out.append(str(yee[i][0]))
                        
                else:
                    out.append(str(yee[i][0]))
                    
            for i in range(0, len(out)):
                out[i] = self._objrepl(out[i], "you", "thou")
                out[i] = self._objrepl(out[i], "your", "thine")
                out[i] = self._objrepl(out[i], "have", "haste")
                out[i] = self._objrepl(out[i], "ahest", "ah")
                out[i] = self._objrepl(out[i], "aheth", "ah")
                out[i] = self._objrepl(out[i], "ahe", "ah")
                out[i] = self._objrepl(out[i], "ise", "is")
                out[i] = self._objrepl(out[i], "rouxls", "Rouxls, The Duketh of Puzzles")
                out[i] = self._objrepl(out[i], "rouxlse", "Rouxls, The Duketh of Puzzles")
                out[i] = self._objrepl(out[i], "Rouxls, The Duketh of Puzzlese", "Rouxls, The Duketh of Puzzles")
                out[i] = self._objrepl(out[i], "the", "thy")
                out[i] = self._objrepl(out[i], "thyre", "there")
                out[i] = self._objrepl(out[i], "thour", "your")
                out[i] = self._objrepl(out[i], "amest", "am")
                out[i] = self._objrepl(out[i], "ameth", "am")
                out[i] = self._objrepl(out[i], "asse", "arse")
                out[i] = self._objrepl(out[i], "real", "reale")
                    
            out = " ".join(out).replace(" '", "'").replace(" .", ".").replace(" ,", ",").replace(" !", "!").replace(" ?", "?")
            
            out = self._objrepl(out, "shuteth up", "shutteth. yon. uppeth.")
            out = self._objrepl(out, "shutest up", "shutteth. yon. uppeth.")
            
            return out
        
        except NameError:
            raise ModuleError("nltk must be installed to use beetroot.texta.rouxls(). Try pip install nltk or pip install beetroot[text].")
            
    def spamton(self, sentence):
        """MAKES YOU [Sound] LIKE [Spamton G. Spamton], THE BEST [[Salesman1997]]!!!!"""
        try:
            yee = pos_tag(sentence.upper().split(" "))
            
            out = []
            for i in range(0, len(yee)):
                if yee[i][1].startswith("NN") or yee[i][1].startswith("VB"):
                    dumb = random.randint(1, 100)
                    if dumb <= 30:
                        out.append("".join(["[", str(yee[i][0]).lower().title(), "]"]))

                    elif dumb > 30 and dumb <= 40:
                        out.append("".join(["[[", str(yee[i][0]).lower().title(), "]]"]))
                        
                    elif dumb > 40 and dumb <= 60:
                        if yee[i][1] == "NN" or yee[i][1] == "NNS":
                            out.append("[[Hyperlink Blocked]]")
                            
                        elif yee[i][1] == "NNPS":
                            nnpsn = [
                                "LIGHT neRs",
                                "DARK neRs",
                                "[Friends]",
                                "[[Hearts]]"
                            ]
                            dumb3 = random.choice(nnpsn)
                            dumb3_1 = random.randint(0, 1)
                            if dumb3_1 == 0:
                                dumb3 = "".join(["[", dumb3, "]"])
                                
                            else:
                                dumb3 = "".join(["[[", dumb3, "]]"])
                                
                            out.append(dumb3)
                            
                        elif yee[i][1] == "NNP":
                            nnpn = [
                                "Kris",
                                "Salesman1997",
                                "Little Sponge",
                                "[[Hyperlink Blocked]]",
                                "[Soul]"
                            ]
                            dumb2 = random.choice(nnpn)
                            dumb2_1 = random.randint(0, 1)
                            if dumb2_1 == 0:
                                dumb2 = "".join(["[", dumb2, "]"])
                                
                            else:
                                dumb2 = "".join(["[[", dumb2, "]]"])
                                
                            out.append(dumb2)
                        
                        else:
                            out.append(str(yee[i][0]))
                        
                    else:
                        out.append(str(yee[i][0]))
                        
                else:
                    out.append(str(yee[i][0]))
                    
            for i in range(0, len(out)):
                out[i] = self._objreplic(out[i], "spamton", "[Spamton G. Spamton]")
                out[i] = self._objreplic(out[i], "strings", "Silly Strings")
                out[i] = self._objreplic(out[i], "soul", "HeartShapedObject")
                out[i] = self._objrepl(out[i], "special", "specil")
                
            out = " ".join(out).replace(" '", "'").replace(" .", ".").replace(" ,", ",").replace(" !", "!").replace(" ?", "?")
            
            return out
            
        except NameError:
            raise ModuleError("nltk must be installed to use beetroot.texta.spamton(). Try pip install nltk or pip install beetroot[text].")
            
    def greek(self, texta):
        """Uses the Greek alphabet to obscure text"""
        greekalpha = list(str("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzΑΒΨΔΕΦΓΗΙΞΚΛΜΝΟΠ:ΡΣΤΘΩ΅ΧΥΖαβψδεφγηιξκλμνοπ;ρστθωςχυζABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzΑΒΨΔΕΦΓΗΙΞΚΛΜΝΟΠ:ΡΣΤΘΩ΅ΧΥΖαβψδεφγηιξκλμνοπ;ρστθωςχυζ"))
        
        texta = list(self._objreplic(self._objreplic(str(texta), "greek", "Ellihnika"), "english", "Agglika"))
        #print(texta)
        for i in range(0, len(texta)):
            try:
                spos = greekalpha.index(texta[i])
                texta[i] = greekalpha[spos + 52]
                
            except (ValueError, IndexError):
                pass
            
        return "".join(texta)
    
    def russian(self, texta):
        """Encodes text using Cyrillic alphabet"""
        rusalpha = list(str("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzФИСВУАПРШОЛДЬТЩЗЙКЫЕГМЦЧНЯфисвуапршолдьтщзйкыегмцчняABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzФИСВУАПРШОЛДЬТЩЗЙКЫЕГМЦЧНЯфисвуапршолдьтщзйкыегмцчня"))
        
        texta = list(self._objreplic(self._objreplic(str(texta), "russian", "Heccrqq"), "english", "Ayukqqcrqq"))
        #print(texta)
        for i in range(0, len(texta)):
            try:
                spos = rusalpha.index(texta[i])
                texta[i] = rusalpha[spos + 52]
                
            except (ValueError, IndexError):
                pass
            
        return "".join(texta)
    
    def reverse(self, texta):
        """Reverses a string"""
        return str(texta)[::-1]
    
    def b65536encode(self, texta):
        """Base65536 encoding"""
        try:
            if objtype(texta) == "bytes":
                return base65536.encode(texta).encode("utf-32")
            
            else:
                return base65536.encode(str(texta).encode("utf-8"))
        
        except NameError:
            raise ModuleError("base65536 must be installed to use beetroot.texta.strb65536encode(), try `pip install base65536` or `pip install beetroot[text]`.")
        
    def b65536decode(self, texta):
        """Base65536 decoding"""
        try:
            if objtype(texta) == "bytes":
                return base65536.decode(texta.decode("utf-32"))
            
            else:
                return base65536.decode(texta).decode("utf-8")
        
        except NameError:
            raise ModuleError("base65536 must be installed to use beetroot.texta.strb65536decode(), try `pip install base65536` or `pip install beetroot[text]`.")
                   
    def phoneencode(self, texta, silent:"silent mode"=False) -> "Encoded string":
        """Encodes text using a phonepad"""
        texta = str(texta)
        err = False
        for item in [
            "#",
            "*"
        ]+[str(i) for i in range(0, 10)]:
            if item in texta and not silent:
                if err:
                    pass
                
                else:
                    print("This string can be encoded, but may/will not be decoded properly.")
                    err = True
                
        alpha = [chr(i) for i in range(97, 123)] + [
            "2",
            "2#",
            "2*",
            "3",
            "3#",
            "3*",
            "4",
            "4#",
            "4*",
            "5",
            "5#",
            "5*",
            "6",
            "6#",
            "6*",
            "7",
            "1",
            "7#",
            "7*",
            "8",
            "8#",
            "8*",
            "9",
            "9#",
            "9*",
            "1#",
        ]
            
        for i in range(0, 26):
            texta = texta.replace(alpha[i], alpha[i+26])
            
        return texta
    
    def phonedecode(self, texta) -> "Decoded string":
        """Decodes text from phoneencode()"""
        texta = str(texta)
        alpha = [
            "2",
            "2#",
            "2*",
            "3",
            "3#",
            "3*",
            "4",
            "4#",
            "4*",
            "5",
            "5#",
            "5*",
            "6",
            "6#",
            "6*",
            "7",
            "1",
            "7#",
            "7*",
            "8",
            "8#",
            "8*",
            "9",
            "9#",
            "9*",
            "1#",
        ][::-1] + list(str("abcdefghijklmnopqrstuvwxyz")[::-1])
            
        for i in range(0, 26):
            texta = texta.replace(alpha[i], alpha[i+26])
            
        return texta
    
    def dotify(self, texta:"a string") -> "A dotified string":
        return ".".join(list(texta.upper()) + [""]).replace(". .", ". ").replace(".\n.", ".\n").replace(".\t.", ".\t")
          
    def spaceify(self, texta:"any string") -> "A spaceified string":
        return " ".join(list(texta)).replace(" \n ", "\n").replace(" \t ", "\t")
          
text = text()