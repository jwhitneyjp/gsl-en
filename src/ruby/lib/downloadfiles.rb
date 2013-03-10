require 'icon'

class DownloadFiles

    class Entry

	def initialize(name, path, description)
	    dot_index = name.rindex('.')
	    raise("Can't handle files without an extension: #{path}") if
		dot_index < 1
	    @name = name[0..(dot_index - 1)]
	    @extension = name[(dot_index + 1)..-1]
	    @path = path
	    @description = description
	end

	attr_reader :name, :extension, :path, :description

	def size
	    if File.size(path) < 1048576 
	        "#{(File.size(path) / 1024) + 1} kb"
	    else
	        "#{(File.size(path) / 1048576) + 1} MB"
	    end
	end

	attr_accessor :zip_size

	def <=>(other)
	    name <=> other.name
	end

	def links_html
	    if not extension.match(/(zip|tgz)$/)
	        " &nbsp;&nbsp; " + link_html(extension, size) +
	        " &nbsp; " + link_html('zip', zip_size)
	    else
	        " &nbsp; " + link_html(extension, size)
	    end
	end

	def link_html(extension, size)
	    "<a href='#{name}.#{extension}' title='#{extension}'>" +
	    "<img style='padding-top:2px;' src='#{Icon.uri_for(extension)}' alt='#{extension}' />" + 
		"</a> <span style='font-size:smaller;'>(#{size})</span>"
	end

    end

    def initialize(globs_descs = [])
	@display_obsolete_link = false
	@paths = []
	@globs_descs = globs_descs
    end

    attr_reader :globs_descs, :entries
    attr_accessor :display_obsolete_link

    def add(path)
	(File.basename(path) == 'download.files') ?
	    parse_download_files(path) :
	    @paths << path
    end

    def has_files
	!entries.empty? || display_obsolete_link
    end

    def html
	html_lines = entries.sort.collect { |e|
	    "<p>#{e.description}<br />#{e.links_html}"
	}
	if @display_obsolete_link
	    html_lines << "<p><small>Earlier files (now out of date) " +
		"<a href='obsolete'>are available for reference</a>.</small></p>"
	end
	html_lines.join("\n")
    end

    def scan_and_install_files(install_dir)
	scan_files
	entries.each { |e|
	    FileUtils.cp(e.path, install_dir)
	    unless e.path.match(/\.(tar\.gz|zip)$/)
	        zip_file = "#{install_dir}/#{e.name}.zip"
	        zip_command = "zip -q -j #{zip_file} #{e.path}"
	        system(zip_command) || raise("Can't execute: #{zip_command}")
		if File.size(zip_file) < 1048576 
                    e.zip_size = "#{(File.size(zip_file) / 1024) + 1} kb"
		else
                    e.zip_size = "#{(File.size(zip_file) / 1048576) + 1} MB"
		end
	    end
	}
    end

    def scan_files
	@entries = @paths.collect { |path|
	    name = File.basename(path)
	    glob_descr = @globs_descs.detect { |g, d| File.fnmatch(g, name) }
	    if glob_descr
	        descr = glob_descr[1]
	        version = name.match(/(([0-9][-.0-9])*[0-9]+[a-z]*)[^0-9]*$/)
		version = version[1].gsub('-','.') if version
		descr = descr.gsub('@@version@@',version) if version
	        Entry.new(name, path, descr)
	    end
	}.compact
    end

    def parse_download_files(path)
	gd = read_download_files_lines(path).
	    collect { |line| line.split(':', 2) }
	@globs_descs = gd + @globs_descs
    end

    def read_download_files_lines(path)
	IO.readlines(path)
    end

end
