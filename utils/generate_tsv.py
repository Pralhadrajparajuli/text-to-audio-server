import csv

# Complete data
data = [
    ('voice001', 'अ:'),
    ('voice002', 'अ'),
    ('voice003', 'अाै'),
    ('voice004', 'आ'),
    ('voice005', 'इ'),
    ('voice006', 'ई'),
    ('voice007', 'उ'),
    ('voice008', 'ऊ'),
    ('voice009', 'ए'),
    ('voice010', 'ऐ'),
    ('voice011', 'ओ'),
    ('voice012', 'क'),
    ('voice013', 'का'),
    ('voice014', 'काै'),
    ('voice015', 'कि'),
    ('voice016', 'की'),
    ('voice017', 'कु'),
    ('voice018', 'कू'),
    ('voice019', 'के'),
    ('voice020', 'कै'),
    ('voice021', 'को'),
    ('voice022', 'क्'),
    ('voice023', 'ख'),
    ('voice024', 'खा'),
    ('voice025', 'खाै'),
    ('voice026', 'खि'),
    ('voice027', 'खी'),
    ('voice028', 'खु'),
    ('voice029', 'खू'),
    ('voice030', 'खे'),
    ('voice031', 'खै'),
    ('voice032', 'खो'),
    ('voice033', 'ख्'),
    ('voice034', 'ग'),
    ('voice035', 'गा'),
    ('voice036', 'गाै'),
    ('voice037', 'गि'),
    ('voice038', 'गी'),
    ('voice039', 'गु'),
    ('voice040', 'गू'),
    ('voice041', 'गे'),
    ('voice042', 'गै'),
    ('voice043', 'गो'),
    ('voice044', 'ग्'),
    ('voice045', 'घ'),
    ('voice046', 'घा'),
    ('voice047', 'घाै'),
    ('voice048', 'घु'),
    ('voice049', 'घू'),
    ('voice050', 'धे'),
    ('voice051', 'घै'),
    ('voice052', 'घो'),
    ('voice053', 'घ्'),
    ('voice054', 'च'),
    ('voice055', 'चा'),
    ('voice056', 'ची'),
    ('voice057', 'चि'),
    ('voice058', 'चु'),
    ('voice059', 'चू'),
    ('voice060', 'चे'),
    ('voice061', 'चै'),
    ('voice062', 'चो'),
    ('voice063', 'च्'),
    ('voice064', 'छ'),
    ('voice065', 'छि'),
    ('voice066', 'छी'),
    ('voice067', 'छु'),
    ('voice068', 'छू'),
    ('voice069', 'छे'),
    ('voice070', 'छै'),
    ('voice071', 'छो'),
    ('voice072', 'छ्'),
    ('voice073', 'जाै'),
    ('voice074', 'जि'),
    ('voice075', 'जी'),
    ('voice076', 'जु'),
    ('voice077', 'जू'),
    ('voice078', 'जे'),
    ('voice079', 'जै'),
    ('voice080', 'जो'),
    ('voice081', 'ज्'),
    ('voice082', 'झ'),
    ('voice083', 'झा'),
    ('voice084', 'झाै'),
    ('voice085', 'झि'),
    ('voice086', 'झी'),
    ('voice087', 'झु'),
    ('voice088', 'झू'),
    ('voice089', 'झे'),
    ('voice090', 'झै'),
    ('voice091', 'झो'),
    ('voice092', 'झ्'),
    ('voice093', 'ञ'),
    ('voice094', 'ञा'),
    ('voice095', 'ञाै'),
    ('voice096', 'ञि'),
    ('voice097', 'ञी'),
    ('voice098', 'ञु'),
    ('voice099', 'ञू'),
    ('voice100', 'ञे'),
    ('voice101', 'ञै'),
    ('voice102', 'ञो'),
    ('voice103', 'ञ्'),
    ('voice104', 'ट'),
    ('voice105', 'टा'),
    ('voice106', 'टाै'),
    ('voice107', 'टि'),
    ('voice108', 'टी'),
    ('voice109', 'टु'),
    ('voice110', 'टू'),
    ('voice111', 'टे'),
    ('voice112', 'टै'),
    ('voice113', 'टो'),
    ('voice114', 'ट्'),
    ('voice115', 'ठ'),
    ('voice116', 'ठा'),
    ('voice117', 'ठाै'),
    ('voice118', 'ठि'),
    ('voice119', 'ठी'),
    ('voice120', 'ठु'),
    ('voice121', 'ठू'),
    ('voice122', 'ठे'),
    ('voice123', 'ठै'),
    ('voice124', 'ठो'),
    ('voice125', 'ठ्'),
    ('voice126', 'ड'),
    ('voice127', 'ड॰'),
    ('voice128', 'ड॰ा'),
    ('voice129', 'ड॰ाै'),
    ('voice130', 'ड॰ि'),
    ('voice131', 'ड॰ी'),
    ('voice132', 'ड॰ु'),
    ('voice133', 'ड॰ू'),
    ('voice134', 'ड॰े'),
    ('voice135', 'ड॰ै'),
    ('voice136', 'ड॰ो'),
    ('voice137', 'ड०्'),
    ('voice138', 'डा'),
    ('voice139', 'डाै'),
    ('voice140', 'डि'),
    ('voice141', 'डी'),
    ('voice142', 'डु'),
    ('voice143', 'डू'),
    ('voice144', 'डे'),
    ('voice145', 'डै'),
    ('voice146', 'डो'),
    ('voice147', 'ड्'),
    ('voice148', 'ढ'),
    ('voice149', 'ढा'),
    ('voice150', 'ढाै'),
    ('voice151', 'ढि'),
    ('voice152', 'ढी'),
    ('voice153', 'ढु'),
    ('voice154', 'ढू'),
    ('voice155', 'ढे'),
    ('voice156', 'ढै'),
    ('voice157', 'ढो'),
    ('voice158', 'ढ्'),
    ('voice159', 'ण'),
    ('voice160', 'णा'),
    ('voice161', 'णाै'),
    ('voice162', 'णि'),
    ('voice163', 'ण'),
    ('voice164', 'णु'),
    ('voice165', 'णू'),
    ('voice166', 'णे'),
    ('voice167', 'णै'),
    ('voice168', 'णो'),
    ('voice169', 'ण्'),
    ('voice170', 'त'),
    ('voice171', 'ता'),
    ('voice172', 'ताै'),
    ('voice173', 'ति'),
    ('voice174', 'ती'),
    ('voice175', 'तु'),
    ('voice176', 'तू'),
    ('voice177', 'ते'),
    ('voice178', 'तै'),
    ('voice179', 'तो'),
    ('voice180', 'त्'),
    ('voice181', 'थ'),
    ('voice182', 'था'),
    ('voice183', 'थाै'),
    ('voice184', 'थि'),
    ('voice185', 'थी'),
    ('voice186', 'थु'),
    ('voice187', 'थू'),
    ('voice188', 'थे'),
    ('voice189', 'थै'),
    ('voice190', 'थो'),
    ('voice191', 'थ्'),
    ('voice192', 'द'),
    ('voice193', 'दा'),
    ('voice194', 'दाै'),
    ('voice195', 'दि'),
    ('voice196', 'दी'),
    ('voice197', 'दु'),
    ('voice198', 'दू'),
    ('voice199', 'दे'),
    ('voice200', 'दै'),
    ('voice201', 'दो'),
    ('voice202', 'द्'),
    ('voice203', 'ध'),
    ('voice204', 'धा'),
    ('voice205', 'धाै'),
    ('voice206', 'धि'),
    ('voice207', 'धी'),
    ('voice208', 'धु'),
    ('voice209', 'धू'),
    ('voice210', 'धे'),
    ('voice211', 'धै'),
    ('voice212', 'धो'),
    ('voice213', 'ध्'),
    ('voice214', 'न'),
    ('voice215', 'ना'),
    ('voice216', 'नाै'),
    ('voice217', 'नि'),
    ('voice218', 'नी'),
    ('voice219', 'नु'),
    ('voice220', 'नू'),
    ('voice221', 'ने'),
    ('voice222', 'नै'),
    ('voice223', 'नो'),
    ('voice224', 'न्'),
    ('voice225', 'प'),
    ('voice226', 'पा'),
    ('voice227', 'पाै'),
    ('voice228', 'पि'),
    ('voice229', 'पी'),
    ('voice230', 'पु'),
    ('voice231', 'पू'),
    ('voice232', 'पे'),
    ('voice233', 'पै'),
    ('voice234', 'पो'),
    ('voice235', 'प्'),
    ('voice237', 'फ'),
    ('voice238', 'फा'),
    ('voice239', 'फाै'),
    ('voice240', 'फि'),
    ('voice241', 'फी'),
    ('voice242', 'फु'),
    ('voice243', 'फू'),
    ('voice244', 'फे'),
    ('voice245', 'फै'),
    ('voice246', 'फो'),
    ('voice246', 'फ्'),
    ('voice247', 'ब'),
    ('voice248', 'बा'),
    ('voice249', 'बाै'),
    ('voice250', 'बि'),
    ('voice251', 'बी'),
    ('voice252', 'बु'),
    ('voice253', 'बू'),
    ('voice254', 'बे'),
    ('voice255', 'बै'),
    ('voice256', 'बो'),
    ('voice257', 'ब्'),
    ('voice258', 'भ'),
    ('voice259', 'भा'),
    ('voice260', 'भाै'),
    ('voice261', 'भि'),
    ('voice262', 'भी'),
    ('voice263', 'भु'),
    ('voice264', 'भू'),
    ('voice265', 'भे'),
    ('voice266', 'भै'),
    ('voice267', 'भो'),
    ('voice268', 'भ्'),
    ('voice269', 'म'),
    ('voice270', 'मा'),
    ('voice271', 'माै'),
    ('voice272', 'मि'),
    ('voice273', 'मी'),
    ('voice274', 'मु'),
    ('voice275', 'मू'),
    ('voice276', 'मे'),
    ('voice277', 'मै'),
    ('voice278', 'मो'),
    ('voice279', 'म्'),
    ('voice280', 'य'),
    ('voice281', 'या'),
    ('voice282', 'याै'),
    ('voice283', 'यि'),
    ('voice284', 'यी'),
    ('voice285', 'यु'),
    ('voice286', 'यू'),
    ('voice287', 'ये'),
    ('voice288', 'यै'),
    ('voice289', 'यो'),
    ('voice290', 'य्'),
    ('voice291', 'र'),
    ('voice292', 'रा'),
    ('voice293', 'राै'),
    ('voice294', 'रि'),
    ('voice295', 'री'),
    ('voice296', 'रु'),
    ('voice297', 'रू'),
    ('voice298', 'रे'),
    ('voice299', 'रै'),
    ('voice300', 'रो'),
    ('voice301', 'र्'),
    ('voice302', 'ल'),
    ('voice303', 'ला'),
    ('voice304', 'लाै'),
    ('voice305', 'लि'),
    ('voice306', 'ली'),
    ('voice307', 'लु'),
    ('voice308', 'लू'),
    ('voice309', 'ले'),
    ('voice310', 'लै'),
    ('voice311', 'लो'),
    ('voice312', 'ल्'),
    ('voice313', 'व'),
    ('voice314', 'वा'),
    ('voice315', 'वाै'),
    ('voice316', 'वि'),
    ('voice317', 'वी'),
    ('voice318', 'वु'),
    ('voice319', 'वू'),
    ('voice320', 'वे'),
    ('voice321', 'वै'),
    ('voice322', 'वो'),
    ('voice323', 'व्'),
    ('voice324', 'श'),
    ('voice325', 'शा'),
    ('voice326', 'शाै'),
    ('voice327', 'शि'),
    ('voice328', 'शी'),
    ('voice329', 'शु'),
    ('voice330', 'शू'),
    ('voice331', 'शे'),
    ('voice332', 'शै'),
    ('voice333', 'शो'),
    ('voice334', 'श्'),
    ('voice335', 'ष'),
    ('voice336', 'षा'),
    ('voice337', 'षाै'),
    ('voice338', 'षि'),
    ('voice339', 'षी'),
    ('voice340', 'षु'),
    ('voice341', 'षू'),
    ('voice342', 'षे'),
    ('voice343', 'षै'),
    ('voice344', 'षो'),
    ('voice345', 'ष्'),
    ('voice347', 'स'),
    ('voice347', 'सं'),
    ('voice348', 'सा'),
    ('voice349', 'साै'),
    ('voice350', 'सि'),
    ('voice351', 'सी'),
    ('voice352', 'सु'),
    ('voice353', 'सू'),
    ('voice354', 'से'),
    ('voice355', 'सै'),
    ('voice356', 'सो'),
    ('voice357', 'स्'),
    ('voice358', 'ह'),
    ('voice359', 'हा'),
    ('voice360', 'हाै'),
    ('voice361', 'हि'),
    ('voice362', 'ही'),
    ('voice363', 'हु'),
    ('voice364', 'हू'),
    ('voice365', 'हे'),
    ('voice366', 'है'),
    ('voice367', 'हो'),
    ('voice368', 'ह्'),
    ('voice369', 'घि'),
    ('voice370', 'घी'),
    ('voice371', 'चाै'),
    ('voice372', 'चि'),
    ('voice373', 'छा'),
    ('voice374', 'छाै'),
    ('voice375', 'ज'),
    ('voice376', 'जा'),
    ('voice377', '१'),
    ('voice378', '२'),
    ('voice379', '३'),
    ('voice380', '४'),
    ('voice381', '५'),
    ('voice382', '६'),
    ('voice383', '७'),
    ('voice384', '८'),
    ('voice385', '९'),
    ('voice386', '०')
]

# voice00000 o
# voice01111 १
# voice02222 २
# voice03333 ३
# voice04444 ४
# voice05555 ५
# voice06666 ६
# voice07777 ७
# voice8888 ८
# voice0999 ९


# voice279 म्
# voice280 य
# voice281 या
# voice282 याै
# voice283 यि
# voice284 यी
# voice285 यु
# voice286 यू
# voice287 ये
# voice288 यै
# voice289 यो
# voice290 य्
# voice291 र
# voice292 रा
# voice293 राै
# voice294 रि
# voice295 री
# voice296 रु
# voice297 रू
# voice298 रे
# voice299 रै
# voice300 रो
# voice301 र्
# voice302 ल
# voice303 ला
# voice304 लाै
# voice305 लि
# voice306 ली
# voice307 लु
# voice308 लू
# voice309 ले
# voice310 लै
# voice311 लो
# voice312 ल्
# voice313 व
# voice314 वा
# voice315 वाै
# voice316 वि
# voice317 वी
# voice318 वु
# voice319 वू
# voice320 वे
# voice321 वै
# voice322 वो
# voice323 व्
# voice324 श
# voice325 शा
# voice326 शाै
# voice327 शि
# voice328 शी
# voice329 शु
# voice330 शू
# voice331 शे
# voice332 शै
# voice333 शो
# voice334 श्
# voice335 ष
# voice336 षा
# voice337 षाै
# voice338 षि
# voice339 षी
# voice340 षु
# voice341 षू
# voice342 षे
# voice343 षै
# voice344 षो
# voice345 ष्
# voice347 स
# voice348 सा
# voice349 साै
# voice350 सि
# voice351 सी
# voice352 सु
# voice353 सू
# voice354 से
# voice355 सै
# voice356 सो
# voice357 स्
# voice358 ह
# voice359 हा
# voice360 हाै
# voice361 हि
# voice362 ही
# voice363 हु
# voice364 हू
# voice365 हे
# voice366 है
# voice367 हो
# voice368 ह्
# voice369 घि
# voice370 घी
# voice371 चाै
# voice372 चि
# voice373 छा
# voice374 छाै
# voice375 ज
# voice376 जा

# File path to save the TSV
file_path = 'syllables_data.tsv'

# Writing to the TSV file
with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(['audio_id', 'sentence'])  # Writing header
    writer.writerows(data)

print(f"TSV file created at {file_path}")