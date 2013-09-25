require 'page'
require 'maruku'

class IndexPage < Page

    def self.parse_content_source_from_dirname(parent, sub_path)
	hb = QAM::HeaderBody.parse_text_file(
	    content_source(sub_path + '/index.txt'))
	text = hb.body
	self.new(parent, hb.header, sub_path, text)
    end

    def initialize(parent, header, sub_path, content)
	sub_path += '/' unless sub_path.match(/\/$/)
	super(parent, header, sub_path)
	@suffix_content_html = Maruku.new( content).to_html
    end

    def css
        if @suffix_content_html.select{|x| x =~ /[^\r\n]/}.first
	    css = "<link href='/en/inc/indexpage-pagecontent.css' rel='stylesheet' type='text/css'/>\n"
	else
	    css = "<link href='/en/inc/indexpage-pageempty.css' rel='stylesheet' type='text/css'/>\n"
        end
	if header['css']
	    css += "<link href='/en/inc/" + header['css'] + "' rel='stylesheet' type='text/css'/>\n"
	end
	css
    end
    
    def content_html
	@content_html ||= (make_content + @suffix_content_html )
    end

    def make_content
    has_subtitles = false
	html_lines = [ "<div class='toc-wrapper'>" ]
	unless children.empty? \
	  or (children.length == 1 and children[0].sub_path.match(/obsolete\/$/)):
	html_lines << "<div class='toc'>"
    if children[0].sub_path.match(/.*\/[0-9][0-9]-T-[^\/]+\/$/)
    html_lines << "<div class='toc-title'>#{children[0].title}</div>"
    children.delete_at(0)
    else
	html_lines << "<div class='toc-title'>Folder contents</div>"
    end
	html_lines << "<ul>"
	    html_lines << children.collect { |child|
		next if child.hidden
        # HACK: for configurable sorting in folder contents box
        if child.sub_path.match(/.*\/[0-9][0-9]-T-[^\/]+\/$/)
          has_subtitles = true
        end
        # Need to detect whether the target file has a URI registered in its
        # metadata. If so, that goes here, and directory-listing-remote gets set below
        # AHA! If title is known, we can also get URI.
        # And AHA again. QAM parses headers in a generic way, all we need to do here
        # is pick up the value.
		uri = "/#{child.sub_path}".sub(/.txt$/, '.html').gsub(/\/[0-9][0-9]-(T-)*/, '/')
        download = dirs.base('src', 'docroot', 'info', child.sub_path + 'download.files' )
		class_name = case child
		    when IndexPage:
		      if File.exists?download 
		          'download-listing'
              elsif child.link
                  uri = child.link
                  if child.link.match(/^\//)
                  'directory-listing-local'
                  else
                  'directory-listing-remote'
                  end
		      else
		          'directory-listing'
		      end
		    when InfoPage:		  'file-listing'
		    else			  ''
		end
        if child.sub_path.match(/.*\/[0-9][0-9]-T-[^\/]+\/$/)
          "</ul><div class='toc-title'>#{child.title}</div><ul>"
        else
          if uri.match(/^\//)
            myuri = "/en" + uri
          else
            myuri = uri
          end
		"<li class='#{class_name}'>" +
		    "<a href=\"#{myuri}\" title=\"#{child.title}\">" +
		    "#{child.title}</a></li>"
        end
	    }
	    html_lines << "</ul></div>"
	end
	if download_files && download_files.has_files
	    html_lines << "<div class='toc'><div class='toc-title'><img src='/en/image/gtk-download.png'> Files for download</div>"
	    html_lines << download_files.html
	    html_lines << "</div>"
	end
	#html_lines << "</div><hr class='clear-left' />"
	html_lines << "</div>"
	html_lines.join("\n")
    end

    def dest_file
	dest_dir('index.html')
    end

    def install_html(template)
    # HACK: for configurable sorting in folder contents box
    install_path = sub_path.gsub(/\/[0-9][0-9]-(T-)*/, '/')
	FileUtils.mkdir_p(dirs.release('docroot', install_path))
	super(template)
    end

end

