import sys 
from PyQt5 import QtWidgets, QtCore 
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager
from qtconsole.console_widget import ConsoleWidget
    
class ConsoleWidget_embed(RichJupyterWidget,ConsoleWidget):
        
   def __init__(self, customBanner=None, *args, **kwargs):
            
      super(ConsoleWidget_embed, self).__init__(*args, **kwargs)
    
      if customBanner is not None:
        self.banner = customBanner
    
   
      self.kernel_manager =                     QtInProcessKernelManager()
      self.kernel_manager.start_kernel(show_banner=True)
      self.kernel_manager.kernel.gui = 'qt'
      self.kernel = self.kernel_manager.kernel
      self.kernel_client = self._kernel_manager.client()
      self.kernel_client.start_channels()
    
      self.print_text("ahmet")
    
   def stop(self):
      self.kernel_client.stop_channels()
      self.kernel_manager.                shutdown_kernel()
      self.guisupport.get_app_qt().exit()
    
      self.exit_requested.connect(self.stop)
    
    
   def push_vars(self, variableDict):
      self.kernel_manager.kernel.shell.push(variableDict)
    
   def clear(self):
      self._control.clear()
    
     
    
   def print_text(self, text):
     
      self._append_plain_text(text, before_prompt=True)
    
   def execute_command(self, command):
      self._execute(command, False)
    
    
if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  main = ConsoleWidget_embed()
  main.print_text("ahmet is king")
  main.show()
  sys.exit(app.exec_())