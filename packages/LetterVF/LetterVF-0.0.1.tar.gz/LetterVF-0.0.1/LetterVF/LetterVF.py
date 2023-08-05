import xlsxwriter as xl
import numpy as np

#read cmudict 
def getPronDict(character, pron_dict_path, removal_list_path=None, addendum_path=None):
    """Create a pronunciation dictionary containing only words which begin with the target letter.
    Args:
        character: target letter
        pron_dict_dath: filepath for the full pronunciation dictionary (i.e., all letters)
        removal_list_path (optional): filepath for a csv file which contains words to be removed from
                                      the pronunciation dictionary
        addendum_path (optional): filepath for a csv file which contains new words (and their pronunciations) 
                                  to be added to the pronunciation dictionary

    Returns:
        pronunciation dictionary containing only words which begin with the target letter
    """
    Dict = []
    with open(pron_dict_path, 'r') as fulldict:
        dictionary = fulldict.readlines()
        #bug probably, i think readlines skips first line
        for word in dictionary:
            #only include desired letter
            if word[0] == character:
                #remove unnecessary characters and append it to preliminary list
                Dict.append(word.replace('\n', '').replace('0', '').replace('1', '').replace('2', '').replace('(', '').replace(')', '').lower())
                #you can probably simplify later code by also using .split()
    if removal_list_path != None:
        Dict = truncatePronDict(Dict, removal_list_path)
    if addendum_path != None:
        Dict = expandPronDict(Dict, addendum_path)
    return Dict


def expandPronDict(pron_dict, addendum_path):
    """Use an addendum csv file to add words to a target letter's pronunciation dictionary.
    Args:
        pron_dict: a target letter's pronunciation dictionary created using getPronDict()
        addendum_path: filepath for a csv file which contains new words (and their pronunciations) 
                       to be added to the pronunciation dictionary
    Returns:
        an updated pronunciation dictionary which contains the new words
    """
    #need to update this to read first line
    with open(addendum_path, 'r') as add_list:
        lines = add_list.readlines()
        lines = [line.strip().strip(',').replace(',', ' ') for line in lines]
        addendum = []
        for line in lines:
            word = ''
            for phon in line:
                word += phon.lower()
            addendum.append(word)
        for item in addendum:
            pron_dict.append(item)
    return pron_dict


def truncatePronDict(pron_dict, removal_list_path):
    """Use a csv file to remove words from a target letter's pronunciation dictionary.
    Args:
        pron_dict: a target letter's pronunciation dictionary created using getPronDict()
        removal_list_path: filepath for a csv file which contains words to be removed from the pronunciation dictionary

    Returns:
        an updated pronunciation dictionary which no longer contains the words to be removed
    """
    #need to update this to read first line
    to_be_removed = []
    with open(removal_list_path, 'r') as rem_list:
        lines = rem_list.readlines()
        # pron_dict = [word for word in pron_dict if word.split()[0].lower() not in [line.strip().lower() for line in lines]]
        for item in pron_dict:
            for line in lines:
                if line.strip().lower() == item.strip().lower().split()[0]:
                    to_be_removed.append(pron_dict.index(item))
    for i in range(len(to_be_removed) -1, -1, -1) :
        pron_dict.remove(pron_dict[to_be_removed[i]])
    return pron_dict


#create list of intrusions
def findIntrusions(pron_dict, data_file_path):
    """Use a target letter's pronunciation dictionary to identify and return a list of intrusions contained in a data file.
    Args:
        pron_dict: a target letter's pronunciation dictionary created using getPronDict()
        data_file_path: filepath for a csv file which contains phonemic VFT data to be analyzed

    Returns:
        a list of intrusions found in a data file
    """
    data = preproc(data_file_path)
    intrusions = []
    pron_dict = [pron_dict[item].split() for item in range(len(pron_dict))]
    word_list = [pron_dict[item][0] for item in range(len(pron_dict))]
    for word in data:
        if word[2] not in word_list:
            intrusions.append(word[2])
    return intrusions


def findPerseverations(data_file_path):
    """Find and return a list of perseverations (i.e., repitions within the same response list) contained in a data file.
    Args:
        data_file_path: filepath for a csv file which contains phonemic VFT data to be analyzed

    Returns:
        a list of perseverations (i.e., repitions within the same response list) contained in a data file
    """
    data = preproc(data_file_path)
    temp_list = []
    perseverations = []
    for word in data:
        if word[2] in temp_list:
            perseverations.append(word)
        else:
            temp_list.append(word[2])
    return perseverations


def preproc(data_file_path):
    """Read data from a data file and return it in a python list that can be used for analysis.
    Args:
        data_file_path: filepath for a csv file which contains phonemic VFT data to be analyzed

    Returns:
        a python list that contains the data from the datafile
    """
    with open(data_file_path, 'r') as data:
        next(data)
        data = data.readlines()
        data = [participant.replace('\n', '').split(',') for participant in data]
        for word in data:
            word[2] = word[2].strip().lower()
    return data


def buildPronList(pron_dict, data_file_path):
    """Return a list of words (and their pronunciations) contained within a data file.
    Args:
        pron_dict: a target letter's pronunciation dictionary created using getPronDict()
        data_file_path: filepath for a csv file which contains phonemic VFT data to be analyzed

    Returns:
        a list of the words (and their pronunciations) contained within a data file
    """
    data = preproc(data_file_path)
    PronunciationList = []
    
    for item in range(len(data)):
        for word in range(len(pron_dict)):
            phon_list = pron_dict[word].split()
            if phon_list[0] in [PronunciationList[i][0] for i in range(len(PronunciationList))]:
                continue
            elif data[item][2] == phon_list[0]:
                PronunciationList.append(phon_list)
    return PronunciationList


def beginningBiphone(word, prev_word):
    """Determine whether two words have the same first 2 phonemes.
    Args:
        word: any word and it's pronunciation as a list of lists
        preword: aany word and it's pronunciation as a list of lists
        
    Returns:
        1 if the two words have the same first 2 phonemes, 0 otherwise
    """
    if word == '' or prev_word == '':
        return 0
    if word[1] == prev_word[1] and word[2] == prev_word[2] and len(word) > 2 and len(prev_word) > 2:
        return 1
    else:
        return 0


def endingBiphone(word, prev_word):
    """Determine whether two words have the same last 2 phonemes.
    Args:
        word: any word and it's pronunciation as a list of lists
        preword: aany word and it's pronunciation as a list of lists

    Returns:
        1 if the two words have the same last 2 phonemes, 0 otherwise
    """
    if word == '' or prev_word == '':
        return 0
    if word[-1] == prev_word[-1] and word[-2] == prev_word[-2] and len(word) > 2 and len(prev_word) > 2:
            return 1
    else:
        return 0


def findRhyme(word):
    """Find the last syllable in a word.
    Args:
        word: any word and it's pronunciation as a list of lists

    Returns:
        the last syllable of a word, or 'no vowel' if the word contains no vowel sounds
    """
    temp = []
    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    i = -1
    for syl in range(len(word)):
        if word[i][0] in vowels:
            temp.append(word[i])
            return temp
        else:
            temp.append(word[i])
            i -= 1
            if word[syl] == word[-1]:
                return 'no vowel'


def rhyme(word, prev_word):
    """Determine whether two words rhyme (i.e., syllabic rhyme).
    Args:
        word: any word and it's pronunciation as a list of lists
        preword: aany word and it's pronunciation as a list of lists

    Returns:
        1 if the two words rhyme syllabically, 0 otherwise
    """
    if word == '' or prev_word == '':
        return 0
    rhyme1 = findRhyme(word)
    rhyme2 = findRhyme(prev_word)
    if word == 'no vowel' or prev_word == 'no vowel':
        return 0
    elif rhyme1 == rhyme2:
        return 1
    else:
        return 0


def firstLetters(word, prev_word, num_of_letters=2):
    """
    Args:
        ToDo

    Returns:
        ToDo
    """
    if word == '' or prev_word == '':
        return 0
    elif len(word[0]) < num_of_letters or len(prev_word[0]) < num_of_letters:
        return 0
    elif word[0][0:num_of_letters] == prev_word[0][0:num_of_letters]:
        return 1
    else:
        return 0


def editDist(word, prev_word, max_dist):
    """
    Args:
        ToDo

    Returns:
        ToDo
    """
#You really need to double check this, had to make some serious edit for levDist in terms of logic
    
    if word == '' or prev_word == '':
        return 0

    word_pron = [syl for syl in word[1:]]
    word_pron.insert(0, ['#'])
    prev_word_pron = [syl for syl in prev_word[1:]]
    prev_word_pron.insert(0, ['#'])
    
    dist_table = np.zeros((len(prev_word_pron), len(word_pron)), dtype=np.int8)
    dist_table[0] = [i for i in range(len(word_pron))]
    dist_table[:,0] = [i for i in range(len(prev_word_pron))]

    if len(word) < 2 and len(prev_word) < 2:
        pass
    elif len(word_pron) < 2 and len(prev_word_pron) >= 2:
        pass
    elif len(prev_word_pron) < 2 and len(word_pron) >= 2:
        pass
    elif word_pron[1] != prev_word_pron[1]:
        dist_table[1,1] = 2

    for col in range(1, len(word_pron)):
        for row in range(1, len(prev_word_pron)):
            if word_pron[col] != prev_word_pron[row]:
                dist_table[row,col] = min(dist_table[row-1,col],dist_table[row,col-1]) + 1
            else:
                dist_table[row,col] = dist_table[row-1,col-1]

    edit_dist = int(dist_table[-1,-1])

    if edit_dist <= max_dist:
        return 1
    else:
        return 0

def levDist(word, prev_word, max_dist):
    """
    Args:
        ToDo

    Returns:
        ToDo
    """
    
    if word == '' or prev_word == '':
        return 0

    word_pron = [syl for syl in word[1:]]
    word_pron.insert(0, ['#'])
    prev_word_pron = [syl for syl in prev_word[1:]]
    prev_word_pron.insert(0, ['#'])
    
    dist_table = np.zeros((len(prev_word_pron), len(word_pron)), dtype=np.int8)
    dist_table[0] = [i for i in range(len(word_pron))]
    dist_table[:,0] = [i for i in range(len(prev_word_pron))]

    if len(word) < 2 and len(prev_word) < 2:
        pass
    elif len(word_pron) < 2 and len(prev_word_pron) >= 2:
        pass
    elif len(prev_word_pron) < 2 and len(word_pron) >= 2:
        pass
    elif word_pron[1] != prev_word_pron[1]:
        dist_table[1,1] = 1

    for row in range(1, len(prev_word_pron)):
        prev_word_prefix = prev_word_pron[0:row+1]
        for col in range(1, len(word_pron)):
            word_prefix = word_pron[0:col+1]
            while len(prev_word_prefix) < len(word_prefix[0:col+1]):
                prev_word_prefix += '#'
            if word_prefix[col] != prev_word_prefix[row]:
                dist_table[row,col] = min(dist_table[row-1,col],dist_table[row,col-1], dist_table[row-1,col-1]) + 1
                # print(f'prev_word_prefix: {prev_word_prefix};   word_prefix:{word_prefix}\n dist: {dist_table[row,col]}')
            else:
                dist_table[row,col] = min(dist_table[row-1,col],dist_table[row,col-1], dist_table[row-1,col-1])
                # print(f'prev_word_prefix: {prev_word_prefix};   word_prefix:{word_prefix}\n dist: {dist_table[row,col]}')

    lev_dist = int(dist_table[-1,-1])

    if lev_dist <= max_dist:
        return 1
    else:
        return 0


def homophone(word, prev_word):
    """
    Args:
        ToDo

    Returns:
        ToDo
    """
    if word == '' or prev_word == '':
        return 0
    if word[0] != prev_word[0] and word[1:] == prev_word[1:]:
        return 1
    else:
        return 0


def isSwitch(clust_list, clust_cats):
    """
    Args:
        ToDo

    Returns:
        ToDo
    """
    first = True
    for item in range(len(clust_list)):
        
        newList = False
        
        if first == True:
            clust_list[item].append(0)
            first = False
            continue
            
        if clust_list[item][0] != clust_list[item-1][0]:
            newList = True
        if clust_list[item][1] != clust_list[item-1][1]:
            newList = True
        
        if newList == True:
            clust_list[item].append(0)
            continue
        
        if 1 in clust_list[item][4:4+clust_cats]:
            clust_list[item].append(0)
        else:
            clust_list[item].append(1)
    
    return clust_list


def checkPerseverations(clust_list):
    """
    Args:
        ToDo

    Returns:
        ToDo
    """
    part_id = clust_list[0][0]
    list_no = clust_list[0][1]
    check_pers = []
    for item in range(len(clust_list)):
        if clust_list[item][0] != part_id or clust_list[item][1] != list_no:
            part_id = clust_list[item][0]
            list_no = clust_list[item][1]
            check_pers = [clust_list[item][2]]
            continue
        elif str(clust_list[item][2]) in check_pers:
            if clust_list[item][3] != '':
                clust_list[item][3] += ', perseveration'
            else:
                clust_list[item][3] = 'perseveration'
        else:
            check_pers.append(clust_list[item][2])
    return clust_list


def clustSize(switch_list):
    """
    Args:
        ToDo

    Returns:
        ToDo
    """
    size = 1
    for item in range(len(switch_list)):
        
        endOfClust = False
        
        if item == len(switch_list)-1:
            switch_list[item].append(size)
            break
        
        elif switch_list[item][0] != switch_list[item+1][0]:
            endOfClust = True
        elif switch_list[item][1] != switch_list[item+1][1]:
            endOfClust = True
        elif switch_list[item+1][-1] == 1:
            endOfClust = True
        
        if endOfClust == True:
            switch_list[item].append(size)
            size = 1
            continue
        else:
            size += 1
            switch_list[item].append('')
            
    return switch_list


def inversePronDict(target_let, pron_dict_path):
    """
    Args:
        ToDo

    Returns:
        ToDo
    """
    Dict = []
    with open(pron_dict_path, 'r') as fulldict:
        dictionary = fulldict.readlines()
        for word in dictionary:
            #only include desired letter
            if word[0] != target_let:
                #remove unnecessary characters and append it to preliminary list
                Dict.append(word.replace('\n', '').replace('0', '').replace('1', '').replace('2', '').replace('(', '').replace(')', '').split())

    return Dict


def intrusionType(intrusion, target_let, pron_dict_path):
    """
    Args:
        ToDo

    Returns:
        ToDo
    """
    pron_dict = inversePronDict(larget_let, pron_dict_path)
    for word in pron_dict:
        if intrusion[1] == word[1]:
            return 'sensible intrusion'
        else:
            return 'intrusion'


def findClusters(pron_dict, data_file_path, include_beg_biphone=True, include_end_biphone=True, include_rhyme=True, first_letters=None, edit_dist=None, include_homophone=False, lev_dist=None):
    """
    Args:
        ToDo

    Returns:
        ToDo
    """
    data = preproc(data_file_path)
    pron_list = buildPronList(pron_dict, data_file_path)
    clust_list = []
    first = True
    clust_cats = 0
    
    if include_beg_biphone == True:
        clust_cats += 1
    if include_end_biphone == True:
        clust_cats += 1
    if include_rhyme == True:
        clust_cats += 1
    if first_letters != None:
        clust_cats += 1
    if edit_dist != None:
        clust_cats += 1
    if include_homophone == True:
        clust_cats += 1
    if lev_dist != None:
        clust_cats += 1
    
    for item in data:
        
        preList = []
        isInList = False
        
        if any(item[2] in match for match in pron_list):#this is pretty badly written; improve later
            for match in pron_list:
                if item[2] in match:
                    word = match
                    isInList = True
                    break
        else:
            word = ''

        if first == True:
            if isInList == True:
                preList.append(item[0])
                preList.append(item[1])
                preList.append(item[2])
                preList.append('')
                for i in range(clust_cats):
                    preList.append(0)
                clust_list.append(preList)
                prev_word = word 
                first = False
                continue
            else:
                preList.append(item[0])
                preList.append(item[1])
                preList.append(item[2])
                preList.append('intrusion')
                for i in range(clust_cats):
                    preList.append(0)
                clust_list.append(preList)
                prev_word = word 
                first = False
                continue
        
        if isInList == True:
            preList.append(item[0])
            preList.append(item[1])
            preList.append(item[2])
            preList.append('')
            if include_beg_biphone == True:
                preList.append(beginningBiphone(word, prev_word))
            if include_end_biphone == True:
                preList.append(endingBiphone(word, prev_word))
            if include_rhyme == True:
                preList.append(rhyme(word, prev_word))
            if first_letters != None:
                preList.append(firstLetters(word, prev_word, num_of_letters=first_letters))
            if edit_dist != None:
                preList.append(editDist(word, prev_word, edit_dist))
            if include_homophone == True:
                preList.append(homophone(word, prev_word))
            if lev_dist != None:
                preList.append(levDist(word, prev_word, lev_dist))
        else:
            preList.append(item[0])
            preList.append(item[1])
            preList.append(item[2])
            preList.append('intrusion')
            if include_beg_biphone == True:
                preList.append(beginningBiphone(word, prev_word))
            if include_end_biphone == True:
                preList.append(endingBiphone(word, prev_word))
            if include_rhyme == True:
                preList.append(rhyme(word, prev_word))
            if first_letters != None:
                preList.append(firstLetters(word, prev_word, num_of_letters=first_letters))
            if edit_dist != None:
                preList.append(editDist(word, prev_word, edit_dist))
            if include_homophone == True:
                preList.append(homophone(word, prev_word))
            if lev_dist != None:
                preList.append(levDist(word, prev_word, lev_dist))
        
        clust_list.append(preList)
        prev_word = word
    
    #The above is REALLYYY slow, try to fix if possible
    clust_list = isSwitch(clust_list, clust_cats)
    clust_list = checkPerseverations(clust_list)
    clust_list = clustSize(clust_list)
    
    return clust_list


def clustSummary(clust_list, include_intrusions=True):
    """
    Args:
        ToDo

    Returns:
        ToDo
    """
    
    summary = []
    clustSizes = 0
    numItem = 0
    numSwitch = 0
    
    for item in range(len(clust_list)):

        preList = []
        endOfList = False

        if item == len(clust_list)-1:
            preList.append(clust_list[item][0])
            preList.append(clust_list[item][1])
            numSwitch += int(clust_list[item][-2])
            clustSizes += int(clust_list[item][-1])
            if clust_list[item][3] == '':
                numItem += 1
            preList.append(numItem)
            preList.append(numSwitch)
            preList.append(round(clustSizes/(numSwitch+1), 3))
            summary.append(preList)
            continue
        
        if clust_list[item][0] != clust_list[item+1][0]:
            endOfList = True
        if clust_list[item][1] != clust_list[item+1][1]:
            endOfList = True

        if endOfList == True:
            preList.append(clust_list[item][0])
            preList.append(clust_list[item][1])
            numSwitch += int(clust_list[item][-2])
            clustSizes += int(clust_list[item][-1])
            if clust_list[item][3] == '':
                numItem += 1
            preList.append(numItem)
            preList.append(numSwitch)
            preList.append(round(clustSizes/(numSwitch+1), 3))

            clustSizes = 0
            numItem = 0
            numSwitch = 0
            summary.append(preList)
                
        else:
            numSwitch += int(clust_list[item][-2])
            if clust_list[item][-1] != '':
                clustSizes += int(clust_list[item][-1])
            if clust_list[item][3] == '':
                numItem += 1
    
    return summary
#Be sure to utilize include_intrusions--or remove it


def sumExport(clust_list, clust_sum, output_path):
    """
    Args:
        ToDo

    Returns:
        ToDo
    """
    
    workbook = xl.Workbook(output_path)
    ws_clust_sum = workbook.add_worksheet('Analysis_Summary')
    ws_clust_list = workbook.add_worksheet('Clustering_Lists')
    
    for row in range(len(clust_list)):
        for column in range(len(clust_list[row])):
            ws_clust_list.write(
                row,
                column,
                clust_list[row][column]
            )
    for row in range(len(clust_sum)):
        for column in range(len(clust_sum[row])):
            ws_clust_sum.write(
                row,
                column,
                clust_sum[row][column]
            )
    workbook.close()
