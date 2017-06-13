#-*-coding=utf-8-*-
import pdfkit

import os
print(os.getcwd())
os.chdir('laomacodes_files')
print(os.getcwd())
htmls = ['0.html', '1.html', '2.html', '3.html', '4.html', '5.html', '6.html', '7.html', '8.html', '9.html', '10.html', '11.html', '12.html', '13.html', '14.html', '15.html', '16.html', '17.html', '18.html', '19.html', '20.html', '21.html', '22.html', '23.html', '24.html', '25.html', '26.html', '27.html', '28.html', '29.html', '30.html', '31.html', '32.html', '33.html', '34.html', '35.html', '36.html', '37.html', '38.html', '39.html', '40.html', '41.html', '42.html', '43.html', '44.html', '45.html', '46.html', '47.html', '48.html', '49.html', '50.html', '51.html', '52.html', '53.html', '54.html', '55.html', '56.html', '57.html', '58.html', '59.html', '60.html', '61.html', '62.html', '63.html', '64.html', '65.html', '66.html', '67.html', '68.html', '69.html', '70.html', '71.html', '72.html', '73.html', '74.html', '75.html', '76.html', '77.html', '78.html', '79.html', '80.html', '81.html', '82.html', '83.html', '84.html', '85.html', '86.html', '87.html', '88.html']
# htmls = ['0.html', '1.html', '2.html', '3.html', '4.html', '5.html', '6.html', '7.html', '8.html']
pdfkit.from_file(htmls, "laoma.pdf")
