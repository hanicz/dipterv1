import { Serializable } from '../utils/serializable'

export class Folder{
    public id: Number;
    public created: Date;
    public folderName: String;
    public parent: Number;
    public deleted: Date;
}