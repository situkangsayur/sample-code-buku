// Bab 15: struct, impl, dan trait di Rust.
use std::f64::consts::PI;

#[derive(Debug, Clone, Copy, PartialEq)]
struct Point {
    x: f64,
    y: f64,
}

impl Point {
    fn new(x: f64, y: f64) -> Self {
        Point { x, y }
    }
    fn distance(&self, other: &Point) -> f64 {
        ((self.x - other.x).powi(2) + (self.y - other.y).powi(2)).sqrt()
    }
}

trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> &str;
    // method bawaan (default) yang memakai method lain di trait
    fn describe(&self) -> String {
        format!("{} dengan luas {:.2}", self.name(), self.area())
    }
}

struct Circle {
    center: Point,
    r: f64,
}

struct Rectangle {
    w: f64,
    h: f64,
}

impl Shape for Circle {
    fn area(&self) -> f64 {
        PI * self.r * self.r
    }
    fn name(&self) -> &str {
        "Circle"
    }
}

impl Shape for Rectangle {
    fn area(&self) -> f64 {
        self.w * self.h
    }
    fn name(&self) -> &str {
        "Rectangle"
    }
}

fn main() {
    let p = Point::new(0.0, 0.0);
    let q = Point::new(3.0, 4.0);
    println!("{:?} {:?} {}", p, q, p.distance(&q)); // ... 5
    assert_eq!(p.distance(&q), 5.0);
    let shapes: Vec<Box<dyn Shape>> = vec![
        Box::new(Circle { center: p, r: 1.0 }),
        Box::new(Rectangle { w: 2.0, h: 3.0 }),
    ];
    for s in &shapes {
        println!("{}", s.describe());
    }
    assert_eq!(shapes[1].describe(), "Rectangle dengan luas 6.00");
    let c = Circle { center: q, r: 2.0 };
    assert_eq!(c.center, q);
    println!("semua uji lolos");
}
