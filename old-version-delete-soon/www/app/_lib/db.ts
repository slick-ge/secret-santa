import * as fs from "fs";

const DB_FILE_PATH = "./app/_lib/users.json";

let userCollection: User[] = [];

interface User {
  email: string;
  pass: string;
}

function saveDataToFile(data: User[]): void {
  const jsonData = JSON.stringify(data, null, 2);
  fs.writeFileSync(DB_FILE_PATH, jsonData, "utf-8");
}

function loadDataFromFile(): User[] {
  try {
    const jsonData = fs.readFileSync(DB_FILE_PATH, "utf-8");
    return JSON.parse(jsonData);
  } catch (error) {
    return [];
  }
}

userCollection = loadDataFromFile();

function addUser(newUser: User): void {
  userCollection.push(newUser);
  saveDataToFile(userCollection);
}

function getUsers() {
  return userCollection;
}

export { userCollection, addUser, getUsers };
