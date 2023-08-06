class seven_segment_bcd_decoder():
    __screen = None
    __segment = list()
    __decoder_input = {0:[0,0,0,0],
                 1:[0,0,0,1],
                 2:[0,0,1,0],
                 3:[0,0,1,1],
                 4:[0,1,0,0],
                 5:[0,1,0,1],
                 6:[0,1,1,0],
                 7:[0,1,1,1],
                 8:[1,0,0,0],
                 9:[1,0,0,1]};


    def __init__(self,x):
        self.__screen = [[" "," "," "],[" "," "," "],[" "," "," "],[" "," "," "],[" "," "," "]]
        self.__decoder(self.__decoder_input[x]);
        self.__segment.clear();
        return;

    def __screen_display(self):
        print();
        for i in self.__screen:
            for j in i:
                print(j,end=" ");
            print();
        print();
        return;


    def __on(self,seg_array):
        for c in seg_array:
            if(c == 'a'): self.__screen[0][1] = "--";
            elif(c == 'b'): self.__screen[1][2] = " |";
            elif(c == 'c'): self.__screen[3][2] = " |";
            elif(c == 'd'): self.__screen[4][1] = "--";
            elif(c == 'e'): self.__screen[3][0] = "|";
            elif(c == 'f'): self.__screen[1][0] = "|";
            elif(c == 'g'): self.__screen[2][1] = "--";

        self.__screen_display();
        return;



    def __XOR(self,i,j):
        if(i == j): return 0
        else: return 1

    def __XNOR(self,i,j):
        if(i == j): return 1
        else: return 0

    def __a(self,l):
        return (l[1] or l[3] or self.__XNOR(l[0],l[2]));

    def __b(self,l):
        return (l[3] or (not l[2]) or (self.__XNOR(l[1],l[0])));

    def __c(self,l):
        return (l[3] or l[2] or (not l[1]) or l[0]);

    def __d(self,l):
        return (l[3] or (l[1] and (not l[0])) or ((not l[2]) and (not l[0])) or ((not l[2]) and l[1]) or (l[2] and (not l[1]) and l[0]));

    def __e(self,l):
        return ((l[1] and (not l[0])) or ((not l[2]) and (not l[0])));

    def __f(self,l):
        return (l[3] or (l[2] and (not l[1])) or (l[2] and (not l[0])) or ((not l[1]) and (not l[0])));

    def __g(self,l):
        return (l[3] or (l[1] and (not l[0])) or self.__XOR(l[1],l[2]));



    def __decoder(self,l): 
        l.reverse(); 
        if(self.__a(l)): self.__segment.append('a');
        if(self.__b(l)): self.__segment.append('b');
        if(self.__c(l)): self.__segment.append('c');
        if(self.__d(l)): self.__segment.append('d');
        if(self.__e(l)): self.__segment.append('e');
        if(self.__f(l)): self.__segment.append('f');
        if(self.__g(l)): self.__segment.append('g');
        l.reverse();
        print(self.__segment);
        self.__on(self.__segment);
        return;




if __name__ == "__main__":
    while(True):
        n = input("enter a number: ");
        if(n == 'e'): break;
        if(n.isdigit()):
            x = int(n);
            if(x >= 0 and x <=9):
                digital = seven_segment_bcd_decoder(x);
            else:
                print("The given number is not BCD representable");
        else:
            print("not a digit");

    input("\nenter anything to exit")