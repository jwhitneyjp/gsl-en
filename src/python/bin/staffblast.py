#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys,os,os.path
sys.path.append('%s' % (os.path.dirname(sys.argv[0]),))
base = '%s/../../../' % (os.path.dirname(sys.argv[0]),)
pythonlib = base + '/release/lib/python'
sys.path.append(pythonlib)

from pathtool import gslpath
gp = gslpath()




from myExcelerator import *
import os
from email import *
import smtplib
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--fields", dest="fields", default='',
                  help="Comma-delimited list of fields")
parser.add_option("-d", "--dump",
                  dest="dump", default=False,
                  action="store_true",
                  help="Dump to file(s), do not send email")
parser.add_option("-r", "--recipients",
                  dest="recipients", default='',
                  help="Comma-delimited list of recipients, or \"all\"")
parser.add_option("-s", "--subject",
                  dest="subject", default='',
                  help="Optional subject header")
parser.add_option("-m", "--message",
                  dest="message_file",metavar="FILE",
                  help="Name of file containing message text in UTF-8 encoding")
parser.add_option("-l", "--list-recipients",
                  dest="list",
                  action="store_true",
                  help="List recipients")
                  
(options, args) = parser.parse_args()

all_fields  = ['field','phone','office','office_hours','photo_web_ok']
all_fields += ['email','email_disclose_ok','website','degrees','career_history']
all_fields += ['research_interests','memberships','visitorships','publications']
all_fields += ['recommended_readings','preparation_suggestions']

def send (to,message_text,filename,name,url,photofilename=None):

    m = MIMEMultipart.MIMEMultipart()
    m['To'] = to
    m['From'] = 'Frank Bennett <bennett@law.nagoya-u.ac.jp>'
    if options.subject:
        m['Subject'] = options.subject
    else:
        m['Subject'] = 'Staff profile request'
    
    ctype = 'text/plain'
    main_type,sub_type = ctype.split('/')
    
    message_text = message_text.decode('utf8','replace')
    
    message_text = message_text.replace('@@name@@',name)
    message_text = message_text.replace('@@url@@',url)
    
    #message_text = message_text.encode('iso-2022-jp','replace').strip()
        
    a = MIMEText.MIMEText(main_type, sub_type)
    a.set_charset('iso-2022-jp')
    a.set_payload(message_text)
    m.attach(a)

    if filename:
        ctype = 'application/vnd.ms-excel'
        main_type,sub_type = ctype.split('/')
        fh = open('%s' % (filename,),'r')
        a = MIMEBase.MIMEBase(main_type, sub_type)
        a.set_payload(fh.read())
        fh.close()
        Encoders.encode_base64(a)
        a.add_header('Content-Disposition', 'attachment', filename=filename)
        m.attach(a)
    
    if photofilename:
        ctype = photofilename[-3:]
        main_type,sub_type = ctype.split('/')
        fh = open( gp.photo.src(photofilename),'r')
        a = MIMEBase.MIMEBase(main_type, sub_type)
        a.set_payload(fh.read())
        fh.close()
        Encoders.encode_base64(a)
        a.add_header('Content-Disposition', 'attachment', filename=photofilename)
        m.attach(a)

    message = m.as_string()

    s = smtplib.SMTP()
    s.connect()
    s.sendmail('bennett@nagoya-u.jp',to,message)
    #s.sendmail('bennett@nagoya-u.jp','bennett@localhost',message)
    s.close()
    ###
    #if filename in os.listdir('.'):
    #    os.unlink(filename)

workbook = WrappedWorkbook( gp.xls.src('instructors.xls') )
c = workbook.get_sheet()

if not options.message_file and not options.list and not options.dump:
    parser.error("Specify a filename for the message with the -m option")

if options.message_file and not options.list:
    ifh = open( options.message_file, 'r')
    message_text = ifh.read()
    # Validate encoding
    message_text = message_text.decode('utf8').encode('utf8')

recipients = options.recipients.split(',')
if 'all' in recipients:
     if len(recipients) != 1: 
         parser.error('\"all\" must be the sole recipient when designated')
         sys.exit()


         
if not options.fields and not options.list:
    e = """Missing field name.

Valid field names:"""
    for o in c.keylist:
        e = e + "\n  %s" % (o,)
    e = e + "\n photo (special)"
    parser.error(e)
    sys.exit()

fields = options.fields.split(',')
if 'all' in fields:
     if len(fields) != 1: 
         parser.error('\"all\" must be the sole recipient when designated')
         sys.exit()
     else:
         fields = all_fields

for f in fields:
    if not f in c.keylist and not f == 'photo':
        e = """Invalid field name '%s'.
Valid field names:""" % (f,)
        for o in c.keylist:
            e = e + "\n  %s" % (o,)
        e = e + "\n photo (special)"
        parser.error(e)

        sys.exit()

if not options.recipients and not options.list:
    parser.error("Must specify a recipient with the -r option")
    sys.exit()
    
send_profile = True
if 'photo' in fields:
    send_photo = True
    photos = os.listdir('./images')
    fields.remove('photo')
    if len(fields) == 0:
        send_profile = False
else:
    send_photo = False

if not options.list:        
    print "Generating and sending out staff profiles"
    print "  . = profile sent"
    sys.stdout.write('  ')
    sys.stdout.flush()
else:
    print "Staff codes are:"

unlock = Protection()
unlock.cell_locked = False

open_border = Borders()
open_border.top = Borders.MEDIUM
open_border.left = Borders.MEDIUM
open_border.right = Borders.MEDIUM
open_border.bottom = Borders.MEDIUM
open_border.bottom_colour = 0x39
open_border.top_colour = 0x39
open_border.left_colour = 0x39
open_border.right_colour = 0x39

closed_border = Borders()
closed_border.top = 0x01
closed_border.left = 0x01
closed_border.right = 0x01
closed_border.bottom = 0x01
closed_border.bottom_colour = 0x9
closed_border.top_colour = 0x9
closed_border.left_colour = 0x9
closed_border.right_colour = 0x9

top_align = Alignment()
top_align.wrap = Alignment.WRAP_AT_RIGHT
top_align.vert = Alignment.VERT_TOP

center_align = Alignment()
center_align.wrap = Alignment.WRAP_AT_RIGHT
center_align.vert = Alignment.VERT_CENTER

closed_font = Font()
closed_font.colour_index = 150

closed_pattern = Pattern()
closed_pattern.pattern_fore_colour = 150
closed_pattern.pattern = Pattern.SOLID_PATTERN

footnote_pattern = Pattern()
footnote_pattern.pattern_fore_colour = 157
footnote_pattern.pattern = Pattern.SOLID_PATTERN

label_font = Font()
label_font.bold = True
label_font.colour_index = 178

biggish_font = Font()
biggish_font.height = 230

footnote_font = Font()
footnote_font.height = 240
footnote_font.colour_index = 157

label_pattern = Pattern()
label_pattern.pattern_fore_colour = 178
label_pattern.pattern = Pattern.SOLID_PATTERN

hcenter_align = Alignment()
hcenter_align.wrap = Alignment.WRAP_AT_RIGHT
hcenter_align.horz = Alignment.HORZ_CENTER

hcenter_vcenter_align = Alignment()
hcenter_vcenter_align.vert = Alignment.VERT_CENTER
hcenter_vcenter_align.horz = Alignment.HORZ_CENTER


label_style = XFStyle()
label_style.num_format_str = '@'
label_style.font = label_font
label_style.alignment = center_align
label_style.pattern = label_pattern
label_style.borders = closed_border

closed_style = XFStyle()
closed_style.num_format_str = '0'
closed_style.font = closed_font
closed_style.alignment = top_align
closed_style.pattern = closed_pattern
closed_style.borders = closed_border

open_style = XFStyle()
open_style.num_format_str = '0'
open_style.borders = open_border
open_style.font = biggish_font
open_style.alignment = top_align
open_style.protection = unlock

open_text_style = XFStyle()
open_text_style.num_format_str = '@'
open_text_style.borders = open_border
open_text_style.font = biggish_font
open_text_style.alignment = top_align
open_text_style.protection = unlock

header_style = XFStyle()
header_style.num_format_str = '@'
f = Font()
f.height = 400
f.bold = True
f.colour_index = 152
header_style.font = f
header_style.alignment = hcenter_align
header_style.pattern = label_pattern
header_style.borders = closed_border

footnote_style = XFStyle()
footnote_style.num_format_str = '0'
footnote_style.alignment = top_align
footnote_style.pattern = footnote_pattern
footnote_style.borders = closed_border
footnote_style.font = footnote_font

footnote_label_style = XFStyle()
footnote_label_style.num_format_str = '@'
footnote_label_style.alignment = hcenter_vcenter_align
footnote_label_style.pattern = footnote_pattern
footnote_label_style.borders = closed_border
footnote_label_style.font = footnote_font

samplebook = WrappedWorkbook( gp.xls.src('instructor_sample.xls') )
samplesheet = samplebook.get_sheet()
dummies = samplesheet.nextmap()

title = 'スタッフ　プロフィール'.decode('utf8')
stitle = '書き込み例'.decode('utf8')

chui1 = '''
【注意】
'''.decode('utf8').strip()

chui2 = '''
枠内の白い所だけが書き込み可能。
Excelの場合、Alt+Enterで改行が入力可能。
記載事項については下の「書き込み例」に参考。
記載後このファイルを bennett@nagoya-u.jp に送付。
'''.decode('utf8').strip()

while 1:
    try:
        data = c.nextmap()
    except:
        break
    to = data['email']

    staff_code = data['uid']
    
    if options.list:
        print "  %s" % (staff_code,)
        continue
    
    if recipients == ["all"]:
        if not data['email'].strip():
            print "No email for %s, skipping." %staff_code
            continue
    elif not staff_code in recipients:
        continue
    
    filename = '%s.xls' % (staff_code,)

    w = Workbook()
    s = w.add_sheet(title)
    s2 = w.add_sheet('Hidden')
    s3 = w.add_sheet(stitle)
    s.col(0).width = 0x1000
    s.col(1).width = 0x4000
    s3.col(0).width = 0x1000
    s3.col(1).width = 0x4000

    for key in c.keylist:
        pos = c.keymap[key]
        s.write(pos+2,0,c.labels[key],label_style)
        s2.write(pos+2,0,c.keylist[pos],closed_style)
        s3.write(pos+2,0,c.labels[key],label_style)
        d = str(data[key]).decode('utf8','replace').strip()
        d = d.replace(unichr(8216),'\'')
        d = d.replace(unichr(8217),'\'')
        d = d.replace(unichr(8220),'\"')
        d = d.replace(unichr(8211),'-')
        #d = u2u8(d,'replace')[0]
        
        dummy = str(dummies[key]).decode('utf8','replace').strip()
        dummy = dummy.replace(unichr(8216),'\'')
        dummy = dummy.replace(unichr(8217),'\'')
        dummy = dummy.replace(unichr(8220),'\"')
        dummy = dummy.replace(unichr(8221),'\"')
        dummy = dummy.replace(unichr(8211),'-')
        #dummy = dummy.encode('utf8','replace')
        
        photofilename=None
        if send_photo:
            photofilename = data['photo_url'].strip().split('/')[-1]
            if not photofilename in photos:
                photofilename=None
        
        if pos in [c.keymap[x] for x in fields]:
            if key == 'birthdate':
                s.write(pos+2,1,d,open_text_style)
            else:
                s.write(pos+2,1,d,open_style)
            s2.write(pos+2,1,'writeme',closed_style)
        else:
            s.write(pos+2,1,d,closed_style)
            s.row(pos+2).set_height(900)
        s3.write(pos+2,1,dummy,closed_style)
        if (pos+2) == 21:
            s.row(pos+2).set_height(1200)
            s3.row(pos+2).set_height(1200)
        elif (pos+2) == 27:
            s.row(pos+2).set_height(3000)
            s3.row(pos+2).set_height(1200)
        else:
            s.row(pos+2).set_height(900)
            s3.row(pos+2).set_height(1200)

    s.write_merge(0,0,0,1,title,header_style)
    s.row(0).set_height(800)
    s3.write_merge(0,0,0,1,stitle,header_style)
    s3.row(0).set_height(800)
    s.write(1,0,chui1,footnote_label_style)
    s.write(1,1,chui2,footnote_style)
    s.row(1).set_height(1500)
    s3.write(1,0,'',footnote_label_style)
    s3.write(1,1,'',footnote_style)
    
    s2.hidden = True
            
    s.protect = True
    s.wnd_protect = True
    s.obj_protect = True
    s.scen_protect = True
    s.password = "garbage_in"
        
    s3.protect = True
    s3.wnd_protect = True
    s3.obj_protect = True
    s3.scen_protect = True
    s3.password = "garbage_in"
        
    w.save(filename)
    
    if not '@' in to:
        to = '%s@law.nagoya-u.ac.jp' % (to,)
    
    if send_profile:
        url = 'http://www.gsl-nagoya-u.net/faculty/member/gsli%s.html' % (staff_code,)
    else:
        filename = None
        url = '(no url yet available)'
    
    status = {}
    status['Professor'] = '教授'
    status['Associate Professor'] = '准教授'
    status['Designated Professor'] = '特任教授'
    status['Designated Associate Professor'] = '特任准教授'
    status['Assistant Professor'] = '講師'
    status['Designated Assistant Professor'] = '特任講師'
    proper_name = data['proper_name'].split('\n')[0]
    name = '%s%s' % (proper_name, status[data['status']])
    name = name.decode('utf8').encode('iso-2022-jp')

    if send_photo and not send_profile and not photofilename:
        print "Error: no photo available for %s.  Not sending!" %data['uid']
        continue
    
    if not options.dump:
        send(to,message_text,filename,name,url,photofilename=photofilename)
    sys.stdout.write(".")
    sys.stdout.flush()
    

print ""
print "Done"
