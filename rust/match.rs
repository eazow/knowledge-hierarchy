fn main() {
    let day_of_week = 2;

    match day_of_week {
        1 => {
            println!("Its Monday my dudes");
        }
        2 => {
            println!("It's Tuesday my dudes");
        }
        3 => {
            println!("It's Wednesday my dudes");
        }
        4 => {
            println!("It's Thursday my dudes");
        }
        5 => {
            println!("It's Friday my dudes");
        }
        6 => {
            println!("It's Saturday my dudes");
        }
        7 => {
            println!("It's Sunday my dudes");
        }
        _ => {
            println!("Default!")
        }
    }
}
