import { Serializable } from '../utils/serializable'

export class MyFile{
    public id: Number;
    public fileName: String;
    public created: Date;
    public folder: Number;
    public content: String;
    public deleted: Date;
    public version: Number;
}