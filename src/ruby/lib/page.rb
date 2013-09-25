require 'docrootfile'
require 'downloadfiles'
require 'socket'

class Page < DocrootFile

    def self.dirs
	@@qam_install_dirs ||= QAM::Install.new.dirs
    end

    def dirs; self.class.dirs; end

    def self.content_source(path = '')
	dirs.base('src', 'docroot', 'info', path)
    end

    def initialize(parent, header, sub_path)
	super(parent, header)
	@sub_path = sub_path
    end

    attr_reader :sub_path

    def content_source(path = '')
	self.class.content_source(path)
    end

    @@pages_missing_titles = []
    def title
	return header['title'].gsub('&','&amp;').gsub('"', '&quot;') if header['title']
	if parent
	    unless @@pages_missing_titles.include?(self)
		$stderr.puts("WARNING: #{sub_path} has no title.")
		@@pages_missing_titles << self
	    end
	    parent.title
	else
	    "NO DEFAULT TITLE AVAILABLE"
	end
    end

    def pagetitle
	return header['pagetitle'].gsub('&','&amp;') if header['pagetitle']
	return header['title'].gsub('&','&amp;') if header['title']
	if parent
	    unless @@pages_missing_titles.include?(self)
		$stderr.puts("WARNING: #{sub_path} has no title.")
		@@pages_missing_titles << self
	    end
	    parent.title
	else
	    "NO DEFAULT TITLE AVAILABLE"
	end
    end

    def link
      return header['link'] if header['link']
      nil
    end

    def banner_image
	image = header['banner-image'] ||
	    (parent ? parent.banner_image : "NO DEFAULT IMAGE")
	warn("Warning: Cannot locate banner-image #{image}") unless
	    File.exists?(dirs.base('src', 'docroot', 'docroot', image))
	image
    end

    def breadcrumbs_html
	parent.breadcrumbs_html +
	    " <span class='breadcrumb'><a href='/en/#{sub_path.gsub(/\/[0-9][0-9]-(T-)*/, '/')}'>#{title}</a></span>&#160;<span style='font-size:larger;'>&#8678;</span>"
    end

    def parent_breadcrumbs_html
	parent.breadcrumbs_html
    end

    def javascript
        if header['javascript']
            "<script type='text/javascript' src='/en/inc/" + header['javascript'] + "'></script>"
	else
	    ''
	end
    end

    def children
        if header['order'] == "reverse"
	    @children ||= make_children.reverse
	else
	    @children ||= make_children
	end
    end

    attr_reader :download_files

    def make_download_files
	@download_files = DownloadFiles.new
    end

    def make_children
	special_ignores = %w[ 00README.txt ]
	@download_files = make_download_files
	children = Dir["#{content_source(sub_path)}*"].collect {
	    |path|
	    child_sub_path = path.gsub(content_source, '')
	    case
	    when special_ignores.include?(File.basename(path))
		nil
	    when File.file?(path + '/index.txt')
		IndexPage.parse_content_source_from_dirname(
		    self, child_sub_path)
	    when path.match(%r'/obsolete$')
		require 'obsoletedownloadspage'
		ObsoleteDownloadsPage.new(self, child_sub_path, @download_files)
	    when File.directory?(path)
		warn("#{path} contains no index.txt")
	    when path.match(%r'/index.txt$')
		nil # this is me
	    when path.match(/\.txt$/)
		InfoPage.parse_content_source_from_file(self, child_sub_path)
	    else
		@download_files.add(path); nil
	    end
      }.compact.sort_by {|a| a.sub_path }
	@download_files.scan_and_install_files(dest_dir)
	children
    end

    def warn(s)
	$stderr.puts(s)
	nil
    end

    def dest_dir(path = '')
      # HACK: for configurable sorting in folder contents box
      dest_path = sub_path.gsub(/\/[0-9][0-9]-(T-)*/, '/')
	  dirs.release('docroot', dest_path, path)
    end

    def <=>(other)
	if self.class == other.class
	    (title || '~') <=> (other.title || '~')
	else
	    case self
		when IndexPage:
		    (other.class == InfoPage) ? 1 : 0
		when InfoPage
		    (other.class == IndexPage) ? -1 : 0
	    end
	end
    end

    def inspect
	"[#{self.class.name} sub_path=#{sub_path.inspect}]"
    end

    def markdown_escape(s)
	s.gsub('_', '\_').
	    gsub('*', '\*').
	    gsub('[', '\[').
	    gsub(']', '\]')
    end

end
