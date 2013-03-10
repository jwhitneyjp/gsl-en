require 'time'

module QAM; class HeaderBody

    def self.parse_text_file(path)
	parse_text(File.open(path) { |s| s.read })
    end

    def self.parse_text(s)
	header = {}
	body = ''
	in_header = true
	s.split(/\r?\n/).each { |line|
	    if in_header
		if line.match(/^$/)
		    in_header = false
		else
		    name, value = line.split(/:\s*/, 2)
		    class << value; include(AsTime); end
		    header[name.downcase] = value
		end
	    else
		body += line + "\n"
	    end
	}
	new(header, body)
    end

    def initialize(header, body)
	@header, @body = header, body
    end

    attr_reader :header, :body

    module AsTime

	def as_time
	    match = self.strip.match(/
		(\d{4}-\d\d-\d\d)
		(?:[ T](\d\d:\d\d(?::\d\d)?)
		    (?:\s?)?(.*)
		)?
		/x)
	    raise(ArgumentError, "Cannot parse date/time: #{self}") unless
		match
	    date = match[1]
	    time = match[2] || '00:00'
	    time += ':00' unless time.length > 5
	    zone = match[3]
	    iso = "#{date}T#{time}#{fix_zone(zone)}"
	    Time.iso8601(iso)
	end

	def fix_zone(zone)
	    return '+00:00' if zone.nil? || zone.strip == ''
	    secs = Time.zone_offset(zone)
	    raise(ArgumentError, "Cannot parse timezone: #{zone}") unless secs
	    hours = secs / 3600
	    unless (secs - (hours * 3600)) == 0
		raise(ArgumentError,
		    "I can't handle the minute offset in time zone #{zone}")
	    end
	    ((hours < 0) ? '-' : '+') + sprintf('%02d', hours.abs) + ':00'
	end

    end

end; end
