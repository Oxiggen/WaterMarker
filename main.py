from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageGrab,ImageFont

CHAR_LIMIT = 20

class Images:

    def __init__(self, root):
        root.title("Watermark Tool")
        #root.geometry("1080x920")
        #root.config(padx=20, pady=20)

        # defining our image canvas
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.canvas = Canvas(root, width=self.screen_width, height=self.screen_height-80, background="gray")
        #self.canvas.pack(fill=BOTH, expand=True) #  configure canvas to occupy the whole main window)
        self.canvas.grid(row=2, column=1, columnspan=4, sticky="NSEW")

        # defining our Upload button
        self.UploadButton = Button(root, text="Upload Image", command=self.ImageUploader)
        #self.UploadButton.pack(padx=20, pady=5)
        self.UploadButton.grid(row=3, column=1, padx=20, sticky="e")


        # defining our Save button
        self.SaveButton = Button(root, text='Save', command=self.ImageSave)
        #self.SaveButton.pack(padx=20, pady=5)
        self.SaveButton.grid(row=3, column=4, sticky="w")

        # defining our input field
        self.inputtxt = Text(root, height=1.3, width=30)
        self.inputtxt.grid(row=3, column=2, padx=2, pady=2, sticky="w")
        self.inputtxt.bind('<KeyRelease>', self.textCheck)  # Key release event to call function.

        # input field button
        self.PrintButton = Button(root, text="Print Watermark", command=self.ImageWaterMark)
        self.PrintButton.grid(row=3, column=2, padx=2, pady=2)

        # defining our Exit button
        self.CloseIcon = Image.open("close.png")
        self.CloseIcon = self.CloseIcon.resize((20, 20))
        self.ResizedIcon = ImageTk.PhotoImage(self.CloseIcon)
        self.CloseButton = Button(root, image=self.ResizedIcon, text='Exit', command=root.destroy)
        #self.CloseButton.pack(padx=10, pady=10)
        self.CloseButton.grid(row=1, column=4, sticky="e")
        # checking the txt length


    def textCheck(self, *args):
        self.my_str = self.inputtxt.get('1.0', 'end-1c')  # The input string except the last line break
        self.breaks = self.my_str.count('\n')  # Number of line breaks ( except the last one )
        self.char_numbers = len(self.my_str) - self.breaks  # Number of chars user has entered
        #print(self.char_numbers)
        #l2.config(text=str(char_numbers))  # display number of chars
        if (self.char_numbers > CHAR_LIMIT):
            self.inputtxt.delete('end-2c')  # remove last char of text widget
            messagebox.showwarning("showwarning", "Maximum 20 characters is allowed.")


    def ImageUploader(self):
        fileTypes = [("Image Files", "*.png;*.jpg")]
        self.path = filedialog.askopenfilename(filetypes=fileTypes)
        print(self.path)
        if len(self.path):
            # if no file is selected, then we are displaying below message
            self.img = Image.open(self.path)
            self.imageWidth , self.imageHeight = self.img.size
            #print(self.imageWidth , self.imageHeight)
            self.pic = ImageTk.PhotoImage(self.img)
            self.canvas.create_image(self.screen_width/2, (self.screen_height-80)/2, image=self.pic)
            return self
        else:
            messagebox.showwarning("showwarning", "No file is chosen !! Please choose a file.")


    def ImageSave(self):
        self.filename = filedialog.asksaveasfile(mode='wb', defaultextension=".jpg", initialdir="/Desktop/", title="Select file", filetypes=(('JPEG', ('*.jpg', '*.jpeg', '*.jpe', '*.jfif')), ('PNG', '*.png')))
        if not self.filename:
            messagebox.showwarning("showwarning", "No path chosen !!")
            return

      # if self.path.endswith(".jpg" or ".jpeg") and self.filename.name.endswith(".png"):
          # self.img = self.img.convert('RGBA')
          # self.img.save(self.filename, 'PNG')

        self.img.save(self.filename)

    def ImageWaterMark(self):
        self.watermarktext = self.inputtxt.get(1.0, "end")

        if len(self.watermarktext) > 1:

            self.font = ImageFont.truetype("Amaranth/Amaranth-Bold.otf", 40)

            #self.textrealWidth = sum(wcwidth.wcwidth(char) for char in self.watermarktext)+1
            self.img2 = Image.new('RGBA', (self.imageWidth, self.imageHeight), (0, 0, 0, 0))
            self.draw2 = ImageDraw.Draw(self.img2)
            #self.ratio = self.imageWidth // self.textWidth
            self.rangeX = self.imageWidth//200
            self.rangeY = self.imageHeight//100

            i = 0
            while i < self.rangeX:
                j = 0
                self.draw2.text((((self.imageWidth // self.rangeX) * i), (self.imageHeight // self.rangeY) * j), text=f"{self.watermarktext}",
                                font=self.font, fill=(223, 223, 223, 100))

                while j < self.rangeY:
                    self.draw2.text((((self.imageWidth // self.rangeX) * i), (self.imageHeight // self.rangeY) * (j+1)), text=f"{self.watermarktext}",
                                font=self.font, fill=(223, 223, 223, 100))
                    j += 1
                i+=1


            #self.img2 = self.img2.rotate(45)
            px, py = 10, 10
            sx, sy = self.img2.size
            self.img.paste(im=self.img2, box=(px, py, px + sx, py + sy), mask=self.img2)
            self.picWatermarked = ImageTk.PhotoImage(self.img)
            self.canvas.create_image(self.screen_width / 2, (self.screen_height - 80) / 2, image=self.picWatermarked)

        else:
            messagebox.showwarning("showwarning", "No text in input !!")


if __name__ == '__main__':
    root = Tk()
    root.attributes('-fullscreen', True)  # make main window full-screen
    application = Images(root)
    root.mainloop()
