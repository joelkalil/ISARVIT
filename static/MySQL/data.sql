-- Table to generate the data

-- Insert into rows :
INSERT INTO `rows` (editable, name, last_update, field, creator, preview, creator_avatar, dynamic_image, creator_id, keywords, questions, uses, description) VALUES (false, 'Urology Report', '2021-12-17T02:24:00.000Z', 'Urology', 'Andreis PURIM', 'http://services.epnet.com/getimage.aspx?imageiid=7432', 'https://scontent-cdt1-1.xx.fbcdn.net/v/t1.6435-9/73016392_1274661512720825_8805041118417780736_n.jpg?_nc_cat=101&ccb=1-5&_nc_sid=174925&_nc_ohc=l5ggB89DXWUAX_5KUx1&_nc_ht=scontent-cdt1-1.xx&oh=00_AT9UWpkSKdZ2-KVxzvSAfRFAE6W3eFLY1x8zbOvWiukqyw&oe=61F0A75C', true,  1201, "['Urology','CR']", 17, 15, 'This is a complete urology report made in 2020 for all urology based-scans used by the CHU Lille.');
INSERT INTO `rows` (editable, name, last_update, field, creator, preview, creator_avatar, dynamic_image, creator_id, keywords, questions, uses, description) VALUES (false, 'Respiratory', '2021-12-15T02:24:00.000Z', 'Respiratory', 'Andreis PURIM', 'https://www.researchgate.net/profile/John-Magnussen/publication/13354345/figure/fig2/AS:601775111409672@1520485775964/Lung-scan-in-eight-standard-views-of-8-mm3-block-sizes-involving-42-of-lung-tissue-In.png', 'https://scontent-cdt1-1.xx.fbcdn.net/v/t1.6435-9/73016392_1274661512720825_8805041118417780736_n.jpg?_nc_cat=101&ccb=1-5&_nc_sid=174925&_nc_ohc=l5ggB89DXWUAX_5KUx1&_nc_ht=scontent-cdt1-1.xx&oh=00_AT9UWpkSKdZ2-KVxzvSAfRFAE6W3eFLY1x8zbOvWiukqyw&oe=61F0A75C', false, 1201, "['Respiratory','CR']", 2, 1, 'A public CR created by the CHU Lille for respiratory scans used since 2018. It is release phase');

-- Insert into columns :
INSERT INTO `columns` (id, label, `default`, minWidth, align) VALUES ('favorite', 'Favorite', true, 0, 'center');
INSERT INTO `columns` (id, label, `default`, minWidth, align) VALUES ('name', 'Name', true, 170, 'left');
INSERT INTO `columns` (id, label, `default`, minWidth, align) VALUES ('field', 'Field', true, 100, 'right');
INSERT INTO `columns` (id, label, `default`, minWidth, align) VALUES ('creator', 'Creator', true, 100, 'right');
INSERT INTO `columns` (id, label, `default`, minWidth, align) VALUES ('uses', 'Uses', true, 100, 'right');
INSERT INTO `columns` (id, label, `default`, minWidth, align) VALUES ('last_updated', 'Last Updated', false, 100, 'right');
INSERT INTO `columns` (id, label, `default`, minWidth, align) VALUES ('keywords', 'Keywords', false, 100, 'right');

-- Insert into users :
INSERT INTO `users` (id, username, password, firstName, lastName, email, description, joined, avatar, chips, admin) VALUES (1201, 'andreis', '123', 'Andreis', 'PURIM', 'andreispurim@aaaa.com', 'Student at Centrale Lille', 2021,'https://scontent-cdt1-1.xx.fbcdn.net/v/t1.6435-9/73016392_1274661512720825_8805041118417780736_n.jpg?_nc_cat=101&ccb=1-5&_nc_sid=174925&_nc_ohc=l5ggB89DXWUAX_5KUx1&_nc_ht=scontent-cdt1-1.xx&oh=00_AT9UWpkSKdZ2-KVxzvSAfRFAE6W3eFLY1x8zbOvWiukqyw&oe=61F0A75C', "[{type: 'work', label: 'CHU Lille'},{type: 'study', label: 'Centrale Lille'},{type: 'favorites', label: '0 Favorites'},{type: 'created', label: '0 Created'}]", true);
INSERT INTO `users` (id, username, password, firstName, lastName, email, description, joined, avatar, chips, admin) VALUES (999, 'joel', '123456', 'Joel', 'KALIL', 'joelkalil@gmail.com', 'Student at Centrale Lille and backend developer', 2021, 'https://scontent-cdt1-1.xx.fbcdn.net/v/t39.30808-6/260366569_5212306868785875_56269399324707922_n.jpg?_nc_cat=109&ccb=1-5&_nc_sid=09cbfe&_nc_ohc=wDtOEnIOZO0AX8yJBw6&tn=6Rgr-l9o9b9adB-p&_nc_ht=scontent-cdt1-1.xx&oh=00_AT9FuV-GBAklEaSnIMmibd6aEOR8nSLvjx1EIfXJzwGWJw&oe=61D1DE2D', "[{type: 'study', label: 'Centrale Lille'},{type: 'favorites', label: '0 Favorites'},{type: 'created', label: '0 Created'}]", false);


-- Insert into forms :
--INSERT INTO `forms` 


