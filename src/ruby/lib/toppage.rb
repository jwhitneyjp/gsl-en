require 'page'
require 'indexpage'
require 'infopage'
require 'find'

class TopPage < Page

    def initialize
	hb = QAM::HeaderBody.parse_text_file(content_source('index.txt'))
	super(nil, hb.header, '')
    end

    def dest_file
	dirs.release('docroot', 'index.html')
    end

    def sub_path
	''
    end

    def title
	header['title'] || 'Please set a title header in info/index.txt.'
	header['title']
    end

    def breadcrumbs_html
	"<span class='breadcrumb'><a href='/en/'>Top</a></span> <span style='font-size:larger;'>&#8678;</span>"
    end

    def parent_breadcrumbs_html
	''
    end

    def css
	[''].join("\n")
    end

    def content_html
	@content_html ||= make_content
    end

    DATE_FORMAT = /\d\d\d\d-\d\d-\d\d/

    def make_content
      ''
    end

    def install_html(template)
	FileUtils.mkdir_p(dirs.release('docroot'))
	super(template)
    end

end
