# mbox_to_html
A python script to normalize emails in html (converted from mbox in Thunderbird) for hosting and crawling

## Problem

Newsletters from the departments and offices of the School of Visual Arts are managed through various services—-Emma, MailChimp, Convio, Mailin, etc.--most of which contain content (images and graphics) that are hosted externally, linked from the email and not embedded in the email itself. Often such graphics are information rich, sometimes even constituting the entire content of the emailed newletter. This poses a problem for archiving these emails, since the email service used by the school (Gmail) only ouputs an mbox file that does not contain linked images.

What we need is a way to capture these emails 'live', as it were. 

## Solution

The best way to capture emails displaying their externally hosted content would be to crawl them as though they were web pages. 

This can be done using Archive-It. All that needs to happen is that individual emails be converted to html files (using Thunderbird), these individual html files can them be hosted online, where accessing such files will ensure that linked images display, and crawled in the same manner as a typical website.

## Steps

Mbox files are downloaded from Gmail. Emails are labeled by department, so that each department's newletters are downloaded as a single mbox file.

Mbox files are converted to html using Thunderbird (requires the ImportExportTools add-on). This option may not be sustainable over the long term.

Html files are foldered in this structure:

- TOP FOLDER (I.E., "parent of thunderbird export files")
  - DEPARTMENT SPECIFIC FOLDER OF EMAILS
      - INDEX.HTML
      - MESSAGES
          - UNREFORMATTED HTML OF EMAIL STRAIGHT FROM THUNDERBIRD
          - UNREFORMATTED HTML OF EMAIL STRAIGHT FROM THUNDERBIRD
          - UNREFORMATTED HTML OF EMAIL STRAIGHT FROM THUNDERBIRD
          - ...
    - DEPARTMENT SPECIFIC FOLDER OF EMAILS
        - INDEX.HTML
        - MESSAGES
            - UNREFORMATTED HTML OF EMAIL STRAIGHT FROM THUNDERBIRD
            - UNREFORMATTED HTML OF EMAIL STRAIGHT FROM THUNDERBIRD
            - UNREFORMATTED HTML OF EMAIL STRAIGHT FROM THUNDERBIRD
            - ...


      
