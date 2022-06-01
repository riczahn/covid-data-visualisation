class Formatter:
    def format_numbers(self, data_value, index):
        """
        Formats numbers below one million to use K for thousands (e.g. 700K) and above to use M for millions (e.g. 1M).
        """
        if data_value >= 1_000_000:
            formatter = '{:1.1f}M'.format(data_value * 0.000_001)
        else:
            formatter = '{:1.0f}K'.format(data_value * 0.001)
        return formatter
