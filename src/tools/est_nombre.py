

def est_nombre(s):
    if len(s) == 0:
        return False
    
    if s.isdigit():
        return True
        
    try:
        float(s)
        return True
    except ValueError:
        return False