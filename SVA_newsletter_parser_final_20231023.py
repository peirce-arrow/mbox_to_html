import os
import re
import shutil
import glob
import string
from bs4 import BeautifulSoup


# METHODS SECTION

#For listing files excluding .DS_Store files
def listdirNohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

#normalizes file names and moves them out of 'messages' folder and into main department/office folder
def newsletterFilenameNormalizeAndMove():
    for d in listdirNohidden(orig_dir):
        dir=os.path.join(orig_dir,d)
        for i in listdirNohidden(dir):
            if i.endswith('.html'):
                html_delete=os.path.join(dir,i)
                os.remove(html_delete)
            if not i.endswith('.html'):
                dir2=os.path.join(dir,i)
            for file_name in os.listdir(dir2): 
                normalized=''.join(c for c in file_name if c in string.printable)
                no_space=normalized.replace(' ','_').replace(',','').replace('&','and')
                no_special=re.sub(r'[\!\"\#\$\%\'\(\)\*\+\^\{\}\~\|]+','',no_space)
                no_special=no_special.replace('___','_').replace('__','_').replace('_-_','-')
                dest_filename=re.sub(r'\.(?!html)','',no_special)
                os.rename(os.path.join(dir2,file_name), os.path.join(dir,dest_filename))


#pulls all the directory names of the individual departments from the parent directory
def folders(path):
    for d in os.listdir(path):
        directory = os.path.join(path, d)
        if os.path.isdir(directory):
            yield directory


#pulls filepath for each individual html file
def files(path):
    for i in os.listdir(path):
        filepath = os.path.join(path, i)
        if not i.startswith('.') and i.endswith('.html') and os.path.isfile(filepath):
            yield filepath

#for finding all the attachments and the embedded imgages
def findAttachmentsEmbeddedImages(path):
    n=0
    for d in os.listdir(path):
        dirs=os.path.join(path, d)
        if os.path.isdir(dirs):
            for i in os.listdir(dirs):
                filepath = os.path.join(dirs, i)
                if not i.startswith('.') and os.path.isfile(filepath):
                    with open(filepath,'r', encoding = "unicode_escape") as f:
                        lines = f.readlines()
                        for content in lines:
                            if content.find('Attachments/') != -1:
                                with open(parent_dir[0]+"/newsletters_attach.txt", 'a') as attach_out:
                                    print(i, file=attach_out)
                                attach_out.close()
                            if content.find('EmbeddedImages/') != -1:
                                with open(parent_dir[0]+"/newsletters_embed.txt", 'a') as embed_out:
                                    print(i, file=embed_out)
                                    embed_out.close()
                        f.close()
                        
                    
#for formatting date
def dateReformat(value):
    date2=''.join(value)
    date2=date2.rstrip(date2[-1])
    date3=date2.split('/')
    if int(date3[0])<10:
        date3[0]='0'+date3[0]
    if int(date3[1])<10:
        date3[1]='0'+date3[1]
    date_output='20'+date3[2]+'/'+date3[0]+'/'+date3[1]
    yield date_output

#move files out of individual folders into single folder in order to upload to server
def moveFiles():
    attach_dst=os.path.join(dst_path,'Attachments')
    embed_dst=os.path.join(dst_path,'EmbeddedImages')
    if os.path.exists(dst_path) == False:
        os.mkdir(dst_path)
        os.mkdir(attach_dst)
        os.mkdir(embed_dst)
        for dir in folders(orig_dir):
            attach_src=os.path.join(dir,'Attachments')
            embed_src=os.path.join(dir,'EmbeddedImages')
            all_files = os.listdir(dir)
            for f in all_files:
                src_path=os.path.join(dir, f)
                if os.path.isfile(src_path) and not src_path.endswith('DS_Store'):
                    shutil.copy(src_path, dst_path)
            if os.path.exists(attach_src)==True:
                attachments=glob.glob(attach_src + '/*')
                ii=1
                for file in attachments:
                    filesplit=os.path.split(file)
                    filename=filesplit[1]
                    dupe=os.path.join(attach_dst,filename)
                    if not os.path.exists(dupe):
                        shutil.copy(file,attach_dst)
                    else:
                        print('ALREADY EXISTS AT DESTINATION: '+file)
                        dupe_orig=os.path.basename(os.path.split(filesplit[0])[0])
                        name_no_ext=os.path.splitext(filename)
                        new_name=os.path.join(attach_dst,name_no_ext[0]+'_'+str(ii)+'_'+dupe_orig+name_no_ext[1])
                        shutil.copy(file,new_name)
                        ii+=1
            if os.path.exists(embed_src)==True:
                embeddeds=glob.glob(embed_src + '/*')
                ii=1
                for file in embeddeds:
                    filesplit=os.path.split(file)
                    filename=filesplit[1]
                    dupe=os.path.join(embed_dst,filename)
                    if not os.path.exists(dupe):
                        shutil.copy(file,embed_dst)
                    else:
                        print('ALREADY EXISTS AT DESTINATION: '+file)
                        dupe_orig=os.path.basename(os.path.split(filesplit[0])[0])
                        name_no_ext=os.path.splitext(filename)
                        new_name=os.path.join(embed_dst,name_no_ext[0]+'_'+str(ii)+'_'+dupe_orig+name_no_ext[1])
                        shutil.copy(file,new_name)
                        ii+=1    
    else:
        print(dst_path,' ALREADY EXISTS!')


def metadataExtractor():
    with open(parent_dir[0]+"/newsletter_metadata.tsv", 'w') as out:
        print("URL\t","Department\t","Subject\t","From\t","Date\t","Group\t","Collector", file=out)
        out.close()
    #pulls and normalizes the department name from the directory path, for use as the 'group' in Archive-It
    for dir in folders(orig_dir):
        dept_name = os.path.basename(os.path.normpath(dir))
        dept_name = dept_name.replace("_"," ")
    #for each directory in the parent directory, run the files(path) method
        for file in files(dir):
            with open(file, 'r', encoding = "unicode_escape") as f:
                parsed_f = BeautifulSoup(f, 'html.parser')
                full_html = (parsed_f.body.find('table', {"class": "moz-header-part1 moz-main-header"}))
                email_scrape=re.search(r'From:.<\/b>.*?@.*?(\.[a-z]{2,4}>?(\.[a-z]{2,4})?>?)', str(full_html)).group()
                full_text=full_html.get_text(separator="\t").strip()
                full_text=re.sub(r'[^\x00-\x7F]+',' ', full_text)
                old_date=re.findall(r'\d{1,2}\/\d{1,2}\/\d{2},', full_text)
                full_text=re.sub(r'Date:.\t.*[AM|PM]','', full_text)
                subject_line=re.sub(r'From:.\t.*','', full_text)
                from_line=re.sub(r'From: </b>','', email_scrape)
                if '&lt;' in from_line:
                    from_line=from_line.replace('&lt;','<').replace('\"','')+'>'
                for reformatted_date in dateReformat(old_date):
                    new_date=reformatted_date
                trim_list = ["Subject: \t","\t","\""]
                for key in trim_list:
                    subject_line=subject_line.replace(key,"")
                with open(parent_dir[0]+"/newsletter_metadata.tsv", 'a') as out:
                    print(file.removeprefix(dir),'\t',dept_name,'\t',subject_line,'\t',from_line,'\t',new_date,'\t','SVA Newsletters','\t','School of Visual Arts Archives', file=out) #STILL PRINTING INITIAL '/' IN URL
                    out.close()
                f.close()
                
# COMMANDS SECTION

# the variable 'thunderbird_output' refers to the folder that is created after Thunderbird HTML export
# the variable 'orig_dir' refers to the folder


#sets the parent directory
orig_dir = re.sub(r'\'','', input("Enter fullpath to parent of thunderbird export files: "))
#orig_dir = "/Users/lgiffin/Documents/newsletters_2023/All/" #can we cut the trailing slash??
#thunderbird_output='/Users/laroldgiggins/Downloads/SVA_work/thunderbird_output'
parent_dir=os.path.split(re.sub('\/$','',orig_dir))
dst_path=os.path.join(os.path.dirname(orig_dir),'final_for_upload')

newsletterFilenameNormalizeAndMove()
moveFiles()
findAttachmentsEmbeddedImages(orig_dir)
metadataExtractor()

'''
READ ME

FOLDER STRUCTURE MUST LOOK LIKE THIS

TOP FOLDER (I.E., "parent of thunderbird export files")
    DEPARTMENT SPECIFIC FOLDER OF EMAILS
        INDEX.HTML
        MESSAGES
            UNREFORMATTED HTML OF EMAIL STRAIGHT FROM THUNDERBIRD
            UNREFORMATTED HTML OF EMAIL STRAIGHT FROM THUNDERBIRD
            UNREFORMATTED HTML OF EMAIL STRAIGHT FROM THUNDERBIRD
            ...
    DEPARTMENT SPECIFIC FOLDER OF EMAILS
        INDEX.HTML
        MESSAGES
            UNREFORMATTED HTML OF EMAIL STRAIGHT FROM THUNDERBIRD
            UNREFORMATTED HTML OF EMAIL STRAIGHT FROM THUNDERBIRD
            UNREFORMATTED HTML OF EMAIL STRAIGHT FROM THUNDERBIRD
            ...
    ...

'''