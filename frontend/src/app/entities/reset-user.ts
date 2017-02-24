import { Serializable } from '../utils/serializable'
import { User } from '../utils/user'

export class ResetUser extends User{
    public token: String;
    public repassword: String;
}
