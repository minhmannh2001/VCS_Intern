#include <bits/stdc++.h>

using namespace std;

string username, line;
bool found;
string tokens[8]; // tokens array store information about user extracted from /etc/passwd file

// split string into tokens
void tokenize(string s, string del = " ")
{
    int start = 0;
    int end = s.find(del);
    int index = 0;
    
    while (end != -1) {
        tokens[index] = s.substr(start, end - start);
        index++;
        start = end + del.size();
        end = s.find(del, start);
    }
    tokens[index] = s.substr(start, end - start);
}

int main() {
	cout << "Enter your username: ";
	cin >> username;
	cout << "----------------------------" << endl;
	
	ifstream passwd_file("/etc/passwd");
	found = false;
	
	while (getline(passwd_file, line)) {
		if (line.find(username) != string::npos) {
			found = true;
			break;
		}
	}
	
	if (not found) {
		cout << "Invalid username! Please try again!" << endl;
		exit(0);
	}
	
	cout << "Information about user " << username << ":" << endl;
	tokenize(line, ":");
	
	// id
	cout << "ID: " << tokens[2] << endl;
	// user's home directory
    cout << "Home directory: " << tokens[5] << endl;
	// user's groups
	cout << "User's groups: ";
	ifstream group_file("/etc/group");
	while (getline(group_file, line)) {
	    if (line.find(username) != string::npos) {
	        for (int i = 0; i < line.size(); i++) {
	            if (line[i] == ':')
	                break;
	            cout << line[i];
	        }
	        cout << " ";
	    }
	}
	cout << endl;
	
	// user's shell
	cout << "Shell: " << tokens[6] << endl;
	
	passwd_file.close();
	
	return 0;
}

