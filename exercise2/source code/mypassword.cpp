#include <bits/stdc++.h>
#include <unistd.h>
#include <pwd.h>
#include <shadow.h>

using namespace std;

#define SHADOW_TMP "/etc/shadow_tmp"

string username, input_password, new_password, hashed_current_password, hashed_input_password, hashed_new_password, line;
int start_index, end_index, count1, count2;

string generate_salt() {
	string alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/.";
	srand(time(0));
	int salt_length = 8 + rand() % 10;
	
	string salt = "$6$";
	
	for (int i = 0; i < salt_length; i++) {
		salt += alphabet[rand() % alphabet.size()];
	}
	
	return salt;
}

int main(int argc, char *argv[]) {
    cout << "Change password program." << endl;
    cout << "---------------------------" << endl;
    
    struct passwd *pointer_passwd = getpwuid(getuid());
    
    username = pointer_passwd->pw_name;
    
    // print user name
    cout << "Username: " << username << endl;
    
    cout << "Enter current password: ";
    cin >> input_password;
    
    ifstream shadow_file_in(SHADOW);
    
    bool is_valid_username = false;
    
    while (getline(shadow_file_in, line)) {
    	if (line.find(username) != string::npos) {
    		is_valid_username = true;
    		count1 = 0;
    		for (int i = 0; i <= line.size(); i++) {
    			if (line[i] == ':') {
    				count1++;
    				if (count1 == 1)
    					start_index = i + 1;
    				else if (count1 == 2) {
    				 	end_index = i - 1;
						break;    				
    				}
    			}
    		}
    		hashed_current_password = line.substr(start_index, end_index - start_index + 1);
    		break;
    	}
    }
    
    shadow_file_in.close();
    
    string hash_algorithm_id, salt;
    
    count1 = 0;
    count2 = 0;
    for (int i = 0; i < hashed_current_password.size(); i++) {
    	if (hashed_current_password[i] == '$') {
    		count1++;
    		if (count1 == 1)
    			start_index = i + 1;
    		else if (count1 == 2) {
    			end_index = i - 1;
    			if (count2 == 0) {
    				count2++;
    				hash_algorithm_id = hashed_current_password.substr(start_index, end_index - start_index + 1);
    				count1 = 1;
    				start_index = i + 1;
    			} else if (count2 == 1) {
    				count2++;
    				salt = hashed_current_password.substr(start_index, end_index - start_index + 1);
    				count1 = 1;
    				start_index = i + 1;
    			}
    		}
    	}
    }
    
    salt = "$" + hash_algorithm_id + "$" + salt;
    
    if (is_valid_username == false) {
    	cout << "Invalid username." << endl;
    	exit(0);
    }
    
    hashed_input_password = crypt(input_password.data(), salt.data());
    if (hashed_input_password != hashed_current_password) {
    	cout << "Invalid password." << endl;
    	cout << "-----------Failed-----------" << endl;
    	exit(0);
    }
    
    cout << "Enter new password: ";
    cin >> new_password;
    string new_salt = generate_salt();
    hashed_new_password = crypt(new_password.data(), new_salt.data());
    
    // Save new hashed password to /etc/shadow file
    ofstream shadow_file_tmp_out;
    shadow_file_tmp_out.open(SHADOW_TMP, ios::out);
	
	shadow_file_in.open(SHADOW, ios::in);
	
    while (getline(shadow_file_in, line)) {
    	count1 = 0;
    	if (line.find(username) != string::npos) {
    		string new_entry = username + ":" + hashed_new_password;
    		for (int i = 0; i < line.size(); i++) {
    			if (line[i] == ':') {
    				count1 += 1;
    			}
    			if (count1 == 2) {
    				new_entry = new_entry + line.substr(i, line.size() - i + 1);
    				break;
    			}
    		}
    		shadow_file_tmp_out << new_entry << endl;
    	} else {
    		shadow_file_tmp_out << line << endl;
    	}
    }
    
    shadow_file_in.close();
    shadow_file_tmp_out.close();
    
    remove(SHADOW);
    rename(SHADOW_TMP, SHADOW);
    
    cout << "-----------Done-----------" << endl;
    
    return 0;
}

