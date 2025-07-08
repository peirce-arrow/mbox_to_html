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

Once html files are extracted, the script will move all html files out of the messages folder and into the top-level folder for the particular department.

The script will then normalize all the filenames, removing every character, including emojis, with the exceptions of numbers, letters, dashes, and underscores. This will be important when hosting and crawling the individual html files.

All files (included folders for embedded images and attachments) are then copied to a new directory for upload to a web server.

The script then creates lists of embedded images and attachments. But why?

Then metadata is scraped from the files and formatted in such a way that it can be batch uploaded to Archive-It after the individual html pages are crawled.

Once files are uploaded to the web server, Archive-It crawls the index page. The index page is set to 'private' (or rather, the box next to "Visible to the public" is unchecked). Once the crawl is completed, the metadata file is uploaded, and the individual html files are accessible through the public-facing Archive-It page via the various metadata fields—department name, date, and subject (which we label "SVA Newsletters"). 

The captured html files will display all the proper email-heading information, will include all linked and embedded images, and will link to the proper attachments, which are also crawled.

The URLs for the html files will likely be odd, since they will include the URL of the host (in our case, github.io and neocities.org), but with the index page suppressed, the files can be accessed through the Archive-It metadata.
