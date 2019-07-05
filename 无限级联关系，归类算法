def category_list_element(L1):
    lines = L1
    data = []
    while len(lines)!=0:
        one = lines.pop()
        init = []
        s1 = True
        while len(lines)!=0:
            row = lines.pop()
            union = list(set(one).intersection(set(row)))
            if len(union)>0:
                init.append(list(set(one).union(set(row))))
                s1 = False
                break
            else:
                init.append(row)  
        if s1:
            data.append(one)
        else:
            pass
        lines.extend(init)
        
    return data
    
