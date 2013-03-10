require 'page'
require 'maruku'

class InfoPage < Page

    def self.parse_content_source_from_file(parent, sub_path)
	hb = QAM::HeaderBody.parse_text_file(content_source(sub_path))
	text = hb.body

        self.new(parent, hb.header, sub_path, text)
    end

    def initialize(parent, header, sub_path, content)
	super(parent, header, sub_path)
	@content_markup = content
	@content_html = "<div id='content'>\n" + Maruku.new(content).to_html + "</div>"
    end

    def css
	css = "<link href='/en/inc/infopage.css' rel='stylesheet' type='text/css'>\n"
	if header['css']
            css += "<link href='/en/inc/" + header['css'] + "' rel='stylesheet' type='text/css'>\n"
        end
	css
    end

    def dest_file
	QAM::Install.new.dirs.release(
	    'docroot', sub_path.gsub(/\.txt$/, '.html'))
    end

    attr_reader :content_markup
    attr_reader :content_html

    def children; []; end

end
