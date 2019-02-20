import sublime, sublime_plugin
import os, string
import re

_index_folder_tag =".es_module_finder"

# Es module finder settings
_es_module_finder_settings = "EsModuleFinder.sublime-settings"
_settings = None

def plugin_loaded():
  global _settings
  _settings = sublime.load_settings(_es_module_finder_settings)

class Utility:
  @staticmethod
  def filematch(filenetry, names):
    (d, f) = filenetry
    for n in names:
      filepath = os.path.join(d, f).upper()
      if filepath.find(n) < 0:
        return False
      return True

class Filefinder:
  def __init__(self):
    self.filelist=[]

  def initFileList(self, working_directory):
    self.filelist=[]

    for curdir, sondirs, sonfiles in os.walk(working_directory):
      for f in sonfiles:
        self.filelist.append( (curdir, f) )

    self.found = []

  def searchFile(self, input):
    names = [os.path.join(*input.upper().split('/'))]
    lastdir=''

    for (d, f) in self.filelist:
      if Utility.filematch((d, f), names):
        if d != lastdir:
          lastdir = d

        self.found.append(os.path.join(d, f))

    return

  def resetFound(self):
    self.found = []

  def getFound(self):
    return self.found

  def getFirstFound(self):
    return self.found[0]

  def getCount(self):
    return len(self.found)

class FilefinderSingleton:
  filefinder = None

  @staticmethod
  def getInstance():
    if FilefinderSingleton.filefinder == None:
      FilefinderSingleton.filefinder = Filefinder()
    return FilefinderSingleton.filefinder

##############################################################

class EsModuleFinderListCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.window = self.view.window()

    # Init file indexes
    working_directory = os.path.join(self.window.extract_variables()['folder'])
    FilefinderSingleton.getInstance().initFileList(working_directory)

    # Module paths
    module_paths = self.module_paths()

    # Search for file paths
    for module_path in module_paths:
      FilefinderSingleton.getInstance().searchFile(module_path)

    # Display quick panel
    self.display_quick_panel()

  def module_paths(self):
    result = self.view.find_all(self.es6_module_regex())

    if len(result) == 0:
      return

    module_paths = []

    for region in result:
      matching_line = self.view.substr(region)
      module_path = re.search(self.es6_module_regex(), matching_line).group(1)
      module_paths.append(module_path[1:])

    return module_paths

  def display_quick_panel(self):
    items = []
    for file_path in self.file_paths():
      items.append([
        os.path.basename(file_path),
        file_path
      ])

    self.window.show_quick_panel(
      items,
      self.open_file
    )

  def open_file(self, selected):
    if selected == -1:
      return

    file_path = self.file_paths()[selected]

    if file_path is None or len(file_path) == 0:
      return

    self.window.open_file(file_path)

  def has_found_files(self):
    return FilefinderSingleton.getInstance().getCount() > 0

  def file_paths(self):
    return FilefinderSingleton.getInstance().getFound()

  def es6_module_regex(self):
    return r"\bimport\s+(?:.+\s+from\s+)?[\']([^\']+)[\']"

class EsModuleFinderOpenCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.window = self.view.window()

    # Init file indexes
    working_directory = os.path.join(self.window.extract_variables()['folder'])
    FilefinderSingleton.getInstance().initFileList(working_directory)

    # Search for files
    text = self.get_text_under_cursor()
    module_path = self.find_module_path(text)
    FilefinderSingleton.getInstance().searchFile(module_path)

    if self.has_found_files():
      self.display_quick_panel()

  def get_text_under_cursor(self):
    candidates = []

    for region in self.view.sel():
      # get selected text
      selected_text = self.view.substr(region)

      # get text under cursor
      text_on_cursor = None
      if region.begin() == region.end():
        word = self.view.word(region)
        if not word.empty():
          text_on_cursor = self.view.substr(word)

      candidates.append(text_on_cursor)

    return candidates[0]

  def find_module_path(self, text):
    if text is None or len(text) == 0:
      return

    module_regex = self.regex_from_text(text)
    result = self.view.find_all(module_regex)

    if len(result) > 0:
      matching_line = self.view.substr(result[0])
      return re.search(module_regex, matching_line).group(1)[1:]

  def display_quick_panel(self):
    items = []
    for file_path in self.file_paths():
      items.append([
        os.path.basename(file_path),
        file_path
      ])

    self.window.show_quick_panel(
      items,
      self.open_file
    )

  def open_file(self, selected):
    if selected == -1:
      return

    file_path = self.file_paths()[selected]

    if file_path is None or len(file_path) == 0:
      return

    self.window.open_file(file_path)

  def has_found_files(self):
    return FilefinderSingleton.getInstance().getCount() > 0

  def file_paths(self):
    return FilefinderSingleton.getInstance().getFound()

  def regex_from_text(self, text):
    return r"\bimport\s+(?:.+\s+from\s+)?[\']([^\']+)[\']"
