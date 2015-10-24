class View():
    def days_str(self, num):
        if num==0: return "Sun"
        elif num==1: return "Mon"
        elif num==2: return "Tue"
        elif num==3: return "Wen"
        elif num==4: return "Thu"
        elif num==5: return "Fri"
        elif num==6: return "Sat"
    
    def days_int(self, day):
        if day=='Sun': return 0
        elif day=='Mon': return 1
        elif day=='Tue': return 2
        elif day=='Wen': return 3
        elif day=='Thu': return 4
        elif day=='Fri': return 5
        elif day=='Sat': return 6

    def time_str(self, num):
        half = ""
        if num%2==1: half="30" 
        else: half="00"
        if num<24 : return str(num/2)+":"+half+"am"
        elif num<48 : return str(num/2-12)+":"+half+"pm"

    def time_int(self, hour_minute_m):
        strs = hour_minute_m.strip().split(':')
        hour = int(strs[0])
        minute = int(strs[1][0:2])
        m = strs[1][2:4]
        num=0
        if m=="pm" : num+=24
        num+=hour*2
        if minute==30 : num+=1
        return num

def Test():
    v = View()
    print v.time_str(v.time_int("1:30pm"))


