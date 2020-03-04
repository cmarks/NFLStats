class RegexTester
    def initialize(pattern=nil)
      @pattern = pattern unless pattern.nil?
    end

    attr_accessor :pattern

    def statement=(statement)
        @statement = statement
      end

    def statement
        @statement
    end

  end

  regex = RegexTester.new
  regex.pattern = /^(http:\/\/)?www\.\w+\.(com|edu|org)$/  # from test_arrays.rb
  puts regex.pattern
  regex.statement = "http://www.google.com"
  puts regex.statement
