import os, sys
import py3toolbox as tb


def output_model_summary(model, file=None):
  summary_lines = []
  model.summary(line_length=120, print_fn=lambda x: summary_lines.append(x))
  summary_text = "\n".join(summary_lines)
  if file is not None:
    tb.write_file(file_name=file, text=summary_text, mode="w")
  print (summary_text)  
  return summary_text