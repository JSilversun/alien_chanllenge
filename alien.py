import sys, re 

result=""
class CommandCenter:
    def __init__(self, name, row, col,scale):
        self.name=name
        self.scale=scale
        self.missing_cells=-1
        self.discovered_cells=1
        self.total_cells=1
        self.min_x=col
        self.max_x=col
        self.min_y=row
        self.max_y=row
        self.last_x=col
        self.last_y=row
        self.center=0

 
    def check_bounds(self, name, row, col):
        if self.min_x>col:
            self.min_x=col
        if self.max_x<col:
            self.max_x=col
        self.max_y=row
        self.total_cells=(self.max_x-self.min_x+1)*(self.max_y-self.min_y+1)
        self.discovered_cells+=1
        self.missing_cells=self.total_cells-self.discovered_cells
        self.center_x=round(((self.max_x-self.min_x+1)/2+self.min_x)*self.scale,3)
        self.center_y=round(((self.max_y-self.min_y+1)/2+self.min_y)*self.scale,3)
        
    def check_cell(self, name, row, col):
        if name=="-":
            self.discovered_cells+=1
            self.missing_cells-=1

def destroy_layer(m,command_centers):
    sub_result=""
    layer_centers=[_ for _ in command_centers if _.missing_cells==0]
    for i,command_center in enumerate(layer_centers):
        if command_center.missing_cells==0:
            sub_result+=str(command_center.name)+":"+str(format(command_center.center_y,'.3f'))+","+str(format(command_center.center_x,'.3f'))
            for row in range(command_center.min_y,command_center.max_y+1):
                for col in range(command_center.min_x,command_center.max_x+1):
                    m[row][col]="-"
            if len(layer_centers)>1 and i+1<len(layer_centers):
                sub_result+=";"
            else:
                sub_result+=" "
    return sub_result
def main():
    fname="input.txt"
    lines=[line.rstrip('\r\n') for line in open(fname)]
    n=int(lines[0])
    for i in range(1,n+1):
        ship_dimensions=[float(x) for x in lines[i].split()]
        ship_width=int(ship_dimensions[1])
        ship_height=int(ship_dimensions[0])
        scale=ship_dimensions[2]
        command_centers=[]
        m = [[0 for x in range(ship_width)] for y in range(ship_height)] 
        for row in range(0,ship_width):
            line=re.sub('[^a-zA-Z]+', ' ', lines[row+i+1])
            line=line.split()
            for col in range(0,len(line)):
                m[row][col]=line[col]
                current_center=m[row][col]
                command_center=next((_ for _ in command_centers if _.name==current_center),None)
                #Add de command center if it isn't in the list
                if command_center is None:
                    command_centers.append(CommandCenter(current_center, row, col,scale))
                else:
                    command_center.check_bounds(current_center, row, col)
            
    result=""
    command_centers.sort(key=lambda x: x.missing_cells)
    i=0
    limit=100
    while command_centers>0 and i>limit:
        i+=1
        result+=destroy_layer(m,command_centers)
        command_centers=[_ for _ in command_centers if _.missing_cells!=0]  
        for command_center in command_centers:
            stop=False
            for row in range(command_center.last_y,command_center.max_y+1):
                for col in range(command_center.last_x,command_center.max_x+1):
                    if m[row][col]==command_center.name or m[row][col]=='-':
                        command_center.check_cell(m[row][col],row,col)
                    else:
                        command_center.last_x=col
                        command_center.last_y=row
                        stop=True
                        break
                    if command_center.max_x==command_center.max_x:
                        command_center.last_x=command_center.min_x
                if stop:
                    break
    print(result)

main()


