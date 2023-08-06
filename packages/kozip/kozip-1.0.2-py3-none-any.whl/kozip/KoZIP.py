import json
import os
import re

class KoZIP:
    def __init__(self):
        old_zip_file = os.path.join(os.path.dirname(__file__), "old_zip.json")
        new_zip_file = os.path.join(os.path.dirname(__file__), "new_zip.json")

        self.old_zip = json.loads(''.join(self._readlines(old_zip_file)))
        self.new_zip = json.loads(''.join(self._readlines(new_zip_file)))
    
    def _readlines(self, file):
        for enc in ["utf8", "utf-8-sig", "ansi", "cp949", "euc-kr"]:
            try:
                with open(file, "r", encoding=enc) as f:
                    lines = f.readlines()

                return lines
            except:
                continue
    
        raise Exception("Encoding not found:", file)
    
    def _build(self, dir):
        data = {}
        for file in [f"{dir}/{file}" for file in os.listdir(dir) if file.endswith(".txt")]:
            for line in self._readlines(file)[1:]:
                splits = line.split("|")
                zipcode = splits[0]

                loc1 = splits[1] # 시도
                loc2 = splits[3] # 시군구
                loc3 = splits[8] # 도로명

                loc4 = splits[11] + ('' if (len(splits[12]) == 0 or splits[12] == "0") else ('-' + splits[12])) # 건물번호본번-건물번호부번
                if len(loc4) != 0:
                    loc3 += ' ' + loc4

                loc5 = splits[5] + splits[17] + ('' if len(splits[18]) == 0 else (' ' + splits[18])) # 읍면동, 리
                if len(loc5) != 0:
                    loc3 += '|' + loc5

                if zipcode not in data.keys():
                    data[zipcode] = dict()

                if loc1 not in data[zipcode].keys():
                    data[zipcode][loc1] = dict()

                if loc2 not in data[zipcode][loc1].keys():
                    data[zipcode][loc1][loc2] = []

                data[zipcode][loc1][loc2].append(loc3)

        for zipcode in data.keys():
            for loc1 in data[zipcode].keys():
                for loc2 in data[zipcode][loc1].keys():
                    data[zipcode][loc1][loc2].sort()

        self.new_zip = data
        
        with open("new_zip.json", "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def ZIPtoAddr(self, zipcode, depth=2, format="string"):
        assert format in ["list", "string"], "Invalid param: format"
        
        zipcode = str(zipcode)
        if re.fullmatch("\d{5}", zipcode):
            data = self.new_zip
        elif re.fullmatch("\d{3}-\d{3}", zipcode):
            data = self.old_zip
        elif re.fullmatch("\d{6}", zipcode):
            zipcode = zipcode[0:3] + '-' + zipcode[3:6]
            data = self.old_zip
        else:
            raise Exception("Invalid param: zipcode")
        
        if depth in [1, "1", "시도"]:
            result = []
            for loc1 in data[zipcode].keys():
                if format == "string":
                    result.append(loc1)
                    
                else: # format == "list"
                    result.append([loc1])
                    
        elif depth in [2, "2", "시군구"]:
            result = []
            for loc1 in data[zipcode].keys():
                for loc2 in data[zipcode][loc1]:
                    if format == "string":
                        string = loc1
                        if len(loc2) != 0:
                            string += ' ' + loc2
                            
                        result.append(string)
                        
                    else: # format == "list"
                        result.append([loc1, loc2])
                        
        elif depth in [3, "3", "도로명"]:
            result = []
            for loc1 in data[zipcode].keys():
                for loc2 in data[zipcode][loc1]:
                    for loc3 in data[zipcode][loc1][loc2]:
                        loc3 = loc3.split("|")[0]
                        if format == "string":
                            string = loc1
                            if len(loc2) != 0:
                                string += ' ' + loc2
                            if len(loc3) != 0:
                                string += ' ' + loc3
                                
                            result.append(string)
                            
                        else: # format == "list"
                            result.append([loc1, loc2, loc3])
                            
        elif depth in [4, "4", "full"]:
            result = []
            for loc1 in data[zipcode].keys():
                for loc2 in data[zipcode][loc1]:
                    for loc3 in data[zipcode][loc1][loc2]:
                        loc3, loc4 = loc3.split("|")
                        if len(loc4) != 0:
                            loc3 += ' ' + f"({loc4})"
                            
                        if format == "string":
                            string = loc1
                            if len(loc2) != 0:
                                string += ' ' + loc2
                            if len(loc3) != 0:
                                string += ' ' + loc3
                            
                            result.append(string)
                            
                        else: # format == "list"
                            result.append([loc1, loc2, loc3])
        else:
            raise Exception("Invalid param: depth")
        
        return result
        
