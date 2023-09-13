# Kaspersky Password Manager & Norton Password Manager adapter

The following program has been created in order to solve the issue of import/exporting password from Kaspersky Password Manager to the Norton one. The main problem was that Kaspersky was unable to export a correctly-formatted CSV file, with the right syntax, containing all the credentials saved on the user account.

# How the adapter works

In order to import the credentials from Kaspersky to Norton, you just need to follow these simple steps:

1. Open Kaspersky Password Manager, go to the settings and export all ther credentials in a .txt file.
2. [Download](https://github.com/Salazar34/norton-kaspersky-converter/releases/latest) the latest version of the converter, launch the script and prompt in the name of the exported file.
3. You'll find a file called **output.csv** _(data/output/output.csv)_ containing your credentials exported in the correct way.
4. Launch Norton Password Manager from your browser, go to the settings and import the **output.csv** file.
