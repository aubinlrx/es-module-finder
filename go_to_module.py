import sublime, sublime_plugin
import os, string
import re

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

    self.found = self.filelist

  def searchFile(self, input):
    names = input.split('/')
    lastdir=''
    self.found = []

    for (d, f) in self.filelist:
      if Utility.filematch((d, f), names):
        if d != lastdir:
          lastdir = d

        self.found(os.path.join(d, f))

    return

  def getFound(self):
    return self.found

  def getCount(self):
    return len(self.found)

class FilefinderSingleton:
  filefinder = None

  @staticmethod
  def getInstance():
    if FilefinderSingleton.filefinder == None:
      FilefinderSingleton.filefinder = Filefinder()
    return FilefinderSingleton.filefinder

class GoToModule(sublime_plugin.TextCommand):
  def run(self, edit):
    window = self.view.window()
    working_directory = os.path.join(window.extract_variables()['folder'], 'app', 'assets', 'javascripts')
    FilefinderSingleton.getInstance().initFileList(working_directory)

    for region in self.view.sel():
      # get selected text
      selected_text = self.view.substr(region)

      # get text under cursor
      text_on_cursor = None
      if region.begin() == region.end():
        word = self.view.word(region)
        if not word.empty():
          text_on_cursor = self.view.substr(word)

      candidates = [text_on_cursor]

      # get module file path
      module_path = self.find_module_path(candidates)
      FilefinderSingleton.getInstance().searchFile(module_path)
      print(FilefinderSingleton.getInstance().getCount())
      return
      self.try_open(module_path)

  def find_module_path(self, candidates):
    for text in candidates:
      if text is None or len(text) == 0:
        continue

      module_regex = self.regex_from_text(text)
      result = self.view.find_all(module_regex)

      if len(result) > 0:
        matching_line = self.view.substr(result[0])
        return re.search(module_regex, matching_line).group(1)[1:]

  def try_open(self, module_path):
    window = self.view.window()

    if module_path is None or len(module_path) == 0:
      return

    window.show_quick_panel([module_path], window.open_file)

    return
    self.potential_files = self.get_filename(module_path)
    if len(self.potential_files) == 0:
      return

    print(self.potential_files)

  def regex_from_text(self, text):
    return r"import " + text + " from '(.*)'"


