
<a id="back-to-top"></a>

# ⚡ am-okay CLI
A portable command-line tool for copying and moving files and directories with progress indication.  
Supports **slot operations**, **default operations**, **cut & copy**, **progress bar**, and **JSON persistence**.

---



## 📚 Summary
- [Features](#general-features)  
- [Installation](#installation)   
- [Use cases](#use-cases)   
    - [Use cases (slot operations)](#use-cases-slot-operations)
    - [Use cases (default operations)](#use-cases-default-operations)
    - [Use cases (filesystem information)](#use-cases-filesystem-information)
- [About the Author](#about-the-author)
- [License](#license)


<a id="general-features"></a>

## ✨ General features
- Prepare and execute **copy** and **cut** operations.
- Store operations in **slots** or use a **default operation**.
- Execute multiple operations at once.
- Reset or delete prepared operations.
- Provides a **progress bar** during file transfers.
- Persist prepared operations in **JSON** for later use.
- Fully portable CLI tool.
- Display detailed filesystem information (size, permissions, dates, ...etc) for files and directories.


<a id="installation"></a>

## 💾 Installation

#### ✅ Install via pip (recommended)
`am-okay` is published on **PyPI** and can be installed using the official Python package manager:
```bash
pip install am-okay
```

#### 🛠️ Install from source via pip (quick development/test)
```bash
git clone https://github.com/baldeuniversel/am-okay.git
cd am-okay
pip install -r requirements.txt
```

#### 🛠️ Install from source using Poetry (full development / contribution)
```bash 
git clone https://github.com/baldeuniversel/am-okay.git
cd am-okay
poetry install
poetry run am-okay --help
```

---



<a id="use-cases"></a>

## 🎯 Use cases

<a id="use-cases-slot-operations"></a>

### 🔢 Use cases (slot operations)

#### Prepare a `copy` operation for the slot 0
```bash
am-okay --slot 0 --copy file1.txt file2.txt dirA
```

#### Prepare a `cut` operation for the slot 1
```bash
am-okay --slot 1 --cut dirB file3.txt
```

#### Print the prepared operation stored in the slot 0
```bash
am-okay --slot 0 --stat
```

#### Print prepared operations for slot indices from 0 to 1 (inclusive)
```bash
am-okay --slot 0-1 --stat
```

#### Print the prepared operations stored in slots 0 and 1
```bash
am-okay --slot 0,1 --stat
```

#### Print all the prepared operations stored in slots
```bash
am-okay --slot all --stat
```

#### Execute the prepared operation for the slot 0 (copy)
```bash
am-okay --slot 0 --paste dest/
```

#### Execute the prepared operation for the slot 1 (cut)
```bash
am-okay --slot 1 --paste dest/
```

#### Execute the prepared operations for slot indices from 0 to 1 (inclusive)
```bash
am-okay --slot 0-1 --paste dest/
```

#### Execute the prepared operations stored in slots 0 and 1
```bash
am-okay --slot 0,1 --paste dest/
```

#### Reset/delete the prepared operation for the slot 0
```bash
am-okay --slot 0 --reset
```

#### Reset/delete the prepared operations for slot indices from 0 to 1 (inclusive)
```bash
am-okay --slot 0-1 --reset
```

#### Reset/delete the prepared operations stored in slots 0 and 1 
```bash
am-okay --slot 0,1 --reset
```

#### Reset/delete all prepared operations stored in the slots
```bash
am-okay --slot all --reset
```

<a id="use-cases-default-operations"></a>

## 🏷️ Use cases (default operations)

#### Prepare a `copy` operation
```bash
am-okay --copy file1.txt dirA
```

#### Prepare a `cut` operation
```bash
am-okay --copy file2.txt dirB
```

#### Execute the prepared default operation
```bash
am-okay --paste dest/
```

#### Print the prepared default operation
```bash
am-okay --stat
```

#### Reset/delete the prepared default operation
```bash
am-okay --reset
```

#### Immediate preparation and execution (`copy`)
```bash
am-okay --copy file3.txt dirC --paste dest/
```

#### Immediate preparation and execution (`cut`)
```bash
am-okay --cut file4.txt dirD --paste dest/
```


<a id="use-cases-filesystem-information"></a>

## 📁 Use cases (filesystem information)

#### Display information about a file
```bash
am-okay --info file5.txt
```

#### Display information about a directory
```bash
am-okay --info dirE
```

#### Display information about multiple files or directories
```bash
am-okay --info file6.txt dirF file7.txt dirG
```

---



<a id="about-the-author"></a>

## 👤 About the Author
**Amadou Baldé**  
*Developer/Programmer ... | Open Source Contributor*

#### Connect with me:
- [GitHub](https://github.com/baldeuniversel)  
- [Email](mailto:baldeuniversel@protonmail.com)

Feel free to reach out if you'd like to collaborate on a project or discuss Python development !

---



<a id="license"></a>

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/license/mit) file for details.

---



[🔝 Back to top](#back-to-top) 
