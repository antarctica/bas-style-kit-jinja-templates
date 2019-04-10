class BskTemplates(object):
    templates_version = '0.1.0'
    bsk_version = '0.5.0'

    def __init__(self):
        self.site_title = 'site title'
        self.site_description = 'site description'
        self.site_favicon = 'default'
        self.site_back_to_top_target_id = 'site-top'
        self.site_main_content_target_id = 'site-main-content'
        self.site_styles = []
        self.site_scripts = []
        self.site_analytics = {}
        self.container_classes = []
        self.main_content_classes = []

        self.bsk_styles = [
            {
                'href': f"https://cdn.web.bas.ac.uk/bas-style-kit/{ self.bsk_version }/css/bas-style-kit.min.css",
                'integrity': 'sha256-f1krGfSoxLtD+u0HEHuqF3D5JW27nONtsLkNZ68+hhM='
            }
        ]
        self.bsk_scripts = [
            {
                'href': f"https://cdn.web.bas.ac.uk/js-libs/jquery-3.3.1.min.js",
                'integrity': 'sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8='
            },
            {
                'href': f"https://cdn.web.bas.ac.uk/js-libs/js.cookie-2.1.3.min.js",
                'integrity': 'sha256-EareStqgZTnMUqLWtDkCa3SldvB8NPBY8u5C6ZUMWRc='
            },
            {
                'href': f"https://cdn.web.bas.ac.uk/bas-style-kit/{ self.bsk_version }/js/bas-style-kit.min.js",
                'integrity': 'sha256-ovsRXnHWw8vzEuH6E3/0R44Etu6OISlK9FjEA1mGuUQ='
            }
        ]
        self.bsk_container_classes = ['bsk-container']
        self.bsk_main_content_classes = []

        self.bsk_site_nav_primary = []
        self.bsk_site_nav_secondary = []
        self.bsk_site_nav_launcher = [
            {'title': 'BAS Home', 'href': 'https://www.bas.ac.uk'},
            {'title': 'Discover BAS Data', 'href': 'https://data.bas.ac.uk'}
        ]
        self.bsk_site_nav_launcher_title = 'Part of British Antarctic Survey'
        self.bsk_site_development_phase = 'alpha'
        self.bsk_site_development_phase_custom = {
            'label_classes': []
        }
        self.bsk_site_nav_brand_text = 'site title'
        self.bsk_site_nav_brand_img_href = ''
        self.bsk_site_nav_brand_href = '/'
        self.bsk_site_feedback_href = '#'
        self.bsk_site_footer_ogl_symbol_a_href = 'http://www.nationalarchives.gov.uk/doc/open-government-licence'
        self.bsk_site_footer_ogl_text_href = 'http://www.nationalarchives.gov.uk/doc/open-government-licence'
        self.bsk_site_footer_ogl_text_version = 'v3.0'
        self.bsk_site_footer_policies_cookies_href = '#'
        self.bsk_site_footer_policies_copyright_href = '#'
        self.bsk_site_footer_policies_privacy_href = '#'
