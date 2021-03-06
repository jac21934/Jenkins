import re
import text_tools
from dataclasses import dataclass
import random

from personalities import SuperProdigy, Blorp, Diamond, Fresh, LowNSlow, Shy

# find "XdY +/- Z"
dice_regex = re.compile("\\b((?:[1-9][0-9]*)?d[1-9][0-9]*)\s*([+-]\s*[0-9]+)?\\b")

# find <personality> +/- Z
personality_regex = re.compile("\\b(superprodigy|blorp|diamond|fresh|low\&slow|shy)\s*([+-]\s*[0-9]+)?\\b")

# find whitespace and a plus to remove
plus_whitespace_regex = re.compile("\\s+|\+")

# find "adv" or "dis"
adv_dis_regex = re.compile("\\b(adv|dis)")

personalities = {
                    "superprodigy": SuperProdigy(),
                    "blorp": Blorp(),
                    "diamond": Diamond(),
                    "fresh": Fresh(),
                    "low&slow": LowNSlow(),
                    "shy": Shy()
                }

@dataclass
class DiceResult:
    name: str
    numDice: int
    numSides: int
    mod: int
    resultList: list
    adv: int
    flavor: str

    def getRollName(self) -> str:
        if self.name == "":
            msg = str(self.numDice) + 'd' + str(self.numSides)
        else:
            msg = self.name
        if self.mod > 0:
           msg += "+" + str(self.mod) 
        elif self.mod < 0:
            msg += str(self.mod) 

        if self.adv == 1:
            msg += " with adv"
        elif self.adv == -1:
            msg += " with dis"


        return msg

    def getResults(self) -> str:
        msg = ""
        if self.adv == 0:
            for res in self.resultList:

                msg += str(res)
                if self.numSides == 20:
        
                    if res == 20:
                        msg += " *CRIT*"
                    elif res == 1:
                        msg += " *CRIT FAIL*"
            
                msg += '\n' 

            val = sum(self.resultList)

            sum_msg = ''
            if self.mod != 0:    
                sum_msg += "Sum: " + str(val) + '\n'
                sum_msg += "Modifer: " + str(self.mod) + '\n'
                val += self.mod


            sum_msg  += "Result: " + str(val)
            if self.flavor:
                sum_msg += " (" + self.flavor + ")" + "\n"
            else:
                sum_msg += "\n"

            msg += text_tools.add_bar(sum_msg, "above")

        # Handling advantage and disadvantage seperately with duplicate code
        # right now. Not great
        elif self.adv == 1 or self.adv == -1:
            
            for res in self.resultList:

                for r in res:
                    msg += str(r)
                    if self.numSides == 20:
            
                        if r == 20:
                            msg += " *CRIT*"
                        elif r == 1:
                            msg += " *CRIT FAIL*"
                
                    msg += '\n' 

                if self.adv == 1:
                    adv_message = "Max: " + str(max(res))
                elif self.adv == -1:
                    adv_message = "Min: " + str(min(res))
                else:
                    raise Exception(f"Unknown advantage type {self.adv}")

                if len(self.resultList) == 1:
                    adv_message += '\n'
                    val = 0
                    if self.mod != 0:    
                        adv_message += "Modifer: " + str(self.mod) + '\n'
                        
                    for res in self.resultList:
                        if self.adv == 1:
                            val += max(res)
                        elif self.adv == -1:
                            val += min(res)
                        
                    val += self.mod

                    adv_message  += "Result: " + str(val) + '\n'

                msg += text_tools.add_bar(adv_message, "above")
                    
                msg += '\n'

            if len(self.resultList) > 1:
                sum_msg = ''
                val = 0
 
                for res in self.resultList:
                    if self.adv == 1:
                        val += max(res)
                    elif self.adv == -1:
                        val += min(res)
                sum_msg += "Sum: " + str(val) + '\n'
                if self.mod != 0:    
                    sum_msg += "Modifer: " + str(self.mod) + '\n'
                                            
                val += self.mod

                sum_msg  += "Result: " + str(val) + '\n'

                msg += text_tools.add_bar(sum_msg, "above")

        return msg

def _getMod(msg:str) -> int:
    mod = re.sub(plus_whitespace_regex, '', msg)
    
    return int(mod)

def _getAdv(msg:str) ->int:
    adv = 0

    results = adv_dis_regex.findall(msg)
    

    if results:
        if results[0] == "adv":
            adv = 1
        elif results[0] == "dis":
            adv = -1
        else:
            raise Exception(f"Unknown advantage type {results[0]}")
    return adv

def roll(msg:str, p):
    dice_results = dice_regex.findall(msg)
    dice_results.extend(personality_regex.findall(msg))
    adv = _getAdv(msg)

    response = ""

    dice_list = []

    for res in dice_results:
        personality = None
        flavor = None
        name = ""
        if res[0] in personalities.keys():
            dice_num = 1
            dice_sides = 20
            personality = personalities[res[0]]
            name=res[0].capitalize()
        else:
            dice_num, dice_sides = res[0].split('d')
        if dice_num == "":
            dice_num = 1
        if res[1]:
            mod = _getMod(res[1])
        else:
            mod = 0
        dice_num = int(dice_num)
        dice_sides = int(dice_sides)

        if dice_num > 100:
            raise Exception("Please roll less than 100 dice")

        def roll(personality, dice_sides):
            if personality:
                return personality.roll()
            else:
                return random.randint(1, dice_sides)

        # roll the dice. roll twice for each if rolling with adv or dis
        if adv == 0:
            result_list = [roll(personality, dice_sides) for die in range(dice_num)]
        else:
            result_list = [(roll(personality, dice_sides), roll(personality, dice_sides)) for die in range(dice_num)]

        if personality:
            flavor = personality.flavor()
        diceRoll = DiceResult(name=name,numDice=dice_num, numSides=dice_sides, mod=mod, resultList=result_list, adv=adv, flavor=flavor)

        dice_list.append(diceRoll)

        
    # Build the message to display
    if dice_list:
        response = "Rolling "


        if len(dice_list) == 1:
            response += dice_list[0].getRollName()

        elif len(dice_list) == 2:
            response += dice_list[0].getRollName() +  " and " + dice_list[1].getRollName()

        else:
            for ii in range(len(dice_list)):
                if ii == len(dice_list) - 1:
                    response += "and " + dice_list[ii].getRollName()
                else:
                    response += dice_list[ii].getRollName() + ", "

        if p is not None:
            response += " for " + p["name"]

        response = text_tools.add_bar(response, "below")

        if len(dice_list) > 1:
            for dice in dice_list:
                dice_name = dice.getRollName()
                response += text_tools.add_bar(dice_name, "below")

                response += dice.getResults()
        else:
            response += dice_list[0].getResults()

    else:
        raise Exception("Invalid message format. Please write NdN for dice rolls.")

    return response