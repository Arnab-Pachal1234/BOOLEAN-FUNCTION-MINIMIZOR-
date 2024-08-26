class Row:
    def __init__(self, row, value):
        self.row= row
        self.value = value

    def __repr__(self):
              return f"Row(row_number={self.row}, value={self.value})"
    

def solve(chart, newchart, rows):
    ans = []
    key_set = set(chart.keys())
    
    while len(key_set) > 0:
       
        rows.sort(key=lambda row: row.value, reverse=True)
       
        ans.append(rows[0].row)
        
    
        for i in range(rows[0].value):
            key_set.discard(newchart[rows[0].row][i])
            del chart[newchart[rows[0].row][i]]
        
     
        nowchart = {}
        for j in chart:
            for k in chart[j]:
                if k in nowchart:
                    nowchart[k].append(j)
                else:
                    nowchart[k] = [j]
        newchart = nowchart
        
       
        rows = [Row(i, len(newchart[i])) for i in newchart]
    
    return ans    
    

def refine(my_list,dc_list): # Removes don't care terms from a given list and returns refined list
    res = []
    for i in my_list:
        if int(i) not in dc_list:
            res.append(i)

    res.sort()
    return res


def findEPI(x): # Function to find essential prime implicants from prime implicants chart
    res = []
    for i in x:
        if len(x[i]) == 1:
            res.append(x[i][0]) if x[i][0] not in res else None
    return res


def findVariables(x): # Function to find variables in a meanterm. For example, the minterm --01 has C' and D as variables
    var_list = []
    for i in range(len(x)):
        if x[i] == '0':
            var_list.append(chr(i+65)+"'")
        elif x[i] == '1':
            var_list.append(chr(i+65))
    return var_list


def flatten(x): # Flattens a list
    flattened_items = []
    for i in x:
        flattened_items.extend(x[i])
    return flattened_items

def findminterms(a):
    gaps = a.count('-')
    if gaps == 0:
        return [str(int(a, 2))]

    temp = [a]  # Start with the original string containing '-'
    for i in range(gaps):
        new_temp = []
        for item in temp:
            index = item.find('-')
            if index != -1:
                # Replace the first occurrence of '-' with '0' and '1'
                new_temp.append(item[:index] + '0' + item[index+1:])
                new_temp.append(item[:index] + '1' + item[index+1:])
        temp = new_temp  # Update temp with the new list of strings

    # Convert binary strings to decimal and sort
    ans = [str(int(x, 2)) for x in temp]
    ans.sort()
    return ans



def compare(a,b): # Function for checking if 2 minterms differ by 1 bit only
    c = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            mismatch_index = i
            c += 1
            if c>1:
                return (False,None)
    return (True,mismatch_index)


def removeTerms(_chart,terms): # Removes minterms which are already covered from chart
    for i in terms:
        for j in findminterms(i):
            try:
                del _chart[j]
            except KeyError:
                pass

def row_dominance(chart):
    newchart ={}
    for i in chart :
        for j in chart[i]:
            if j in newchart :
                newchart[j].append(i)
            else :
                newchart[j]=[i]    
    

    rows_to_remove = set() 
    for i in newchart:
        if i in rows_to_remove:
            continue  # Skip rows that are already marked for removal
        for j in newchart:
            if i != j and j not in rows_to_remove:
                # Only compare rows if they are not the same and j hasn't been removed
                if set(newchart[i])<(set(newchart[j])):
                    rows_to_remove.add(i)  # Mark i for removal if it's a subset of j
                    break  # Stop further comparisons for i since it's already dominated

    # Remove dominated rows from the chart
    for i in rows_to_remove:
        for j in newchart[i]:
         print("row dominance occured")
         del chart[j]

    return chart


def column_dominance(chart):

    cols = list(chart.keys())
    cols_to_remove = set()
    
  
    for i in cols:
        if i in cols_to_remove:
            continue
        else :
         for j in cols:
            if i != j and j not in cols_to_remove:
                pi_i = set(chart[i])
              
                pi_j = set(chart[j])
                
             
              
                if pi_i<(pi_j):
                  
                    cols_to_remove.add(j) # remove dominating columns 
    for i in cols_to_remove:
        print("Column_dominace occured in :- %d column ",i)
        del chart[i]
    return chart

mt = [int(i) for i in input("Enter the minterms as decimal of the minterm: ").strip().split()] #strip method is used to remove the leading and trailing spaces
dc = [int(i) for i in input("Enter the don't cares as decimal numbers (If any ): ").strip().split()]

mt.sort()

minterms = mt+dc

minterms.sort()

size = len(bin(minterms[-1]))-2 

groups,all_pi = {},set()

for minterm in minterms:
    count_ones = bin(minterm).count('1') 
    binary_rep = bin(minterm)[2:].zfill(size)  

   
    if count_ones in groups:
        groups[count_ones].append(binary_rep)
    else:
        groups[count_ones] = [binary_rep]



print("\n\n\n\nGroup No.\tMinterms\tBinary of Minterms\n%s"%('='*50))
for i in sorted(groups.keys()):
    
    print("%5d:"%i) 
    
    for j in groups[i]:
        
        print("\t\t    %-20d%s"%(int(j,2),j)) 
    
    print('-'*50) 


while True:
    tmp = groups.copy()
    groups,m,marked,should_stop = {},0,set(),True
    l = sorted(list(tmp.keys()))

    for i in range(len(l)-1):

        for j in tmp[l[i]]:

            for k in tmp[l[i+1]]: 

                res = compare(j,k)

                if res[0]: 

                    if m in groups :

                        if j[:res[1]]+'-'+j[res[1]+1:] not in groups[m]:
                         
                         groups[m].append(j[:res[1]]+'-'+j[res[1]+1:])  
                        else:

                            None 
                    else :
                        groups[m] = [j[:res[1]]+'-'+j[res[1]+1:]] 

                    should_stop = False

                    marked.add(j) 

                    marked.add(k)
        m += 1

    local_unmarked = set(flatten(tmp)).difference(marked)
    
    all_pi = all_pi.union(local_unmarked) 
    
    print("Unmarked elements(Prime Implicants) of this table:"
          ,None if len(local_unmarked)==0 else ', '.join(local_unmarked)) 
    

    if should_stop: 
        print("\n\nAll Prime Implicants: ",None if len(all_pi)==0 else ', '.join(all_pi)) 
        break
    
    print("\n\n\n\nGroup No.\tMinterms\tBinary of Minterms\n%s"%('='*50))
    for i in sorted(groups.keys()):

        print("%5d:"%i) 

        for j in groups[i]:

            print("\t\t%-24s%s"%(','.join(findminterms(j)),j)) 
           
        print('-'*50)




sz = len(str(mt[-1])) 

chart = {}

print('\n\n\nPrime Implicants chart:\n\n    Minterms    |%s\n%s'%(' '.join((' '*(sz-len(str(i))))+str(i) for i in mt),'='*(len(mt)*(sz+1)+16)))

for i in all_pi:
  
    merged_minterms,y = findminterms(i),0
    
    newmerged_minterms = [(int)(merged_minterms[i]) for i in range(len(merged_minterms)) ]
       
    newmerged_minterms.sort()
   
    print("%-16s|"%','.join(merged_minterms),end='')
    
    for j in refine(newmerged_minterms,dc):
       
        x = mt.index(j)*(sz+1)
        
        print(' '*abs(x-y)+' '*(sz-1)+'X',end='')

        y = x+sz

        if j in chart:

            chart[j].append(i) if i not in chart[j] else None 
        else:

            chart[j] = [i]

    print('\n'+'-'*(len(mt)*(sz+1)+16))


EPI = findEPI(chart)

print("\nEssential Prime Implicants: "+', '.join(str(i) for i in EPI))

chart = row_dominance(chart)
chart = column_dominance(chart)

removeTerms(chart,EPI) 
if len(chart)!=0:
      newchart ={}
      for i in chart :
        for j in chart[i]:
            if j in newchart :
                newchart[j].append(i)
            else :
                newchart[j]=[i]    
    
      rows =[Row(i,len(newchart[i])) for i in newchart]
      print(len(rows))
      EPI = solve(chart,newchart,rows)


final_result = [findVariables(i) for i in EPI]

print('\n\nSolution: F = '+' + '.join(''.join(i) for i in final_result))

input("\nPress enter to exit...")


    
