class ObsoleteDownloadsPage < IndexPage

    def hidden; true; end

    def initialize(parent, sub_path, parent_download_files)
	markup = IO.read(
	    dirs.base('src', 'docroot', 'obsolete-downloads-template.txt'))
    if parent.pagetitle
    mytitle = parent.pagetitle
    else
    mytitle = parent.title
    end
	markup = markup.gsub('@@parent-title@@',mytitle)
	super(parent, { 'title' => mytitle + ' (archives)' }, sub_path, markup)
	@parent_download_files = parent_download_files
	@parent_download_files.display_obsolete_link = true
    end

    def make_download_files
	@download_files = DownloadFiles.new(@parent_download_files.globs_descs)
    end

end
