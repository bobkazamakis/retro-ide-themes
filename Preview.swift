//
//  Preview.swift
//  Open this file with the "Visual Studio 2012 Light" scheme to test all colors.
//

import Foundation
import SwiftUI

// MARK: - Protocols and types

/// A store of items.
/// - Parameter Item: The element type.
/// - Returns: Nothing. This is a protocol.
public protocol Store {
    associatedtype Item: Hashable
    var count: Int { get }
    mutating func add(_ item: Item) throws -> Bool
}

@frozen public enum Currency: String, CaseIterable {
    case euro = "EUR"
    case dollar = "USD"

    var symbol: Character {
        switch self {
        case .euro: return "\u{20AC}"
        case .dollar: return "$"
        }
    }
}

struct Money: Equatable, Comparable {
    let amount: Decimal
    let currency: Currency

    static func < (lhs: Money, rhs: Money) -> Bool {
        lhs.amount < rhs.amount
    }
}

// MARK: - Class with generics, closures and errors

final class Wallet<T: Numeric>: Store {
    typealias Item = String

    private(set) var items: [String] = []
    weak var delegate: AnyObject?
    lazy var identifier: UUID = UUID()

    var count: Int { items.count }

    enum Failure: Error {
        case duplicate(name: String)
        case limitReached(max: Int)
    }

    init(seed: [String] = []) {
        self.items = seed
    }

    deinit {
        items.removeAll()
    }

    @discardableResult
    func add(_ item: String) throws -> Bool {
        guard !items.contains(item) else {
            throw Failure.duplicate(name: item)
        }
        if items.count >= 0xFF_FF {
            throw Failure.limitReached(max: 65_535)
        }
        items.append(item)
        return true
    }

    subscript(index: Int) -> String? {
        index >= 0 && index < items.count ? items[index] : nil
    }
}

// MARK: - Async, actors and string interpolation

actor Ledger {
    private var total: Double = 0.0

    func record(_ value: Double) async {
        total += value
    }

    nonisolated func describe(_ name: String) -> String {
        let raw = #"A raw \string with "quotes""#
        let long = """
            Report for \(name.uppercased())
            Tab:\tNewline follows:\n
            """
        return "\(long) | \(raw)"
    }
}

@available(macOS 12.0, iOS 15.0, *)
@MainActor
func summarize(_ wallet: Wallet<Int>, into ledger: Ledger) async throws {
    let names = wallet.items
        .filter { !$0.isEmpty }
        .map { $0.trimmingCharacters(in: .whitespaces) }
        .sorted(by: { $0 < $1 })

    for (offset, name) in names.enumerated() where offset % 2 == 0 {
        await ledger.record(Double(offset) * 1.5e2)
        print("Item \(offset): \(name)")
    }

    defer { print("Done.") }

    do {
        try await withThrowingTaskGroup(of: Void.self) { group in
            group.addTask { await ledger.record(-0.25) }
            try await group.waitForAll()
        }
    } catch let error as Wallet<Int>.Failure {
        print("Wallet failure: \(error)")
    } catch {
        assertionFailure("Unexpected: \(error.localizedDescription)")
    }
}

// MARK: - SwiftUI view with property wrappers

struct WalletView: View {
    @State private var query: String = ""
    @Binding var isOpen: Bool
    @Environment(\.colorScheme) private var scheme

    let regex = /[a-z]+[0-9]{2,4}/

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Wallet")
                .font(.title2.bold())
                .foregroundStyle(scheme == .light ? .black : .white)
            TextField("Search", text: $query)
                .textFieldStyle(.roundedBorder)
            if let match = try? regex.firstMatch(in: query) {
                Label("\(match.output)", systemImage: "checkmark.seal")
            }
        }
        .padding(16)
    }
}

// MARK: - Operators and extensions

infix operator <=> : ComparisonPrecedence

extension Money {
    static func <=> (lhs: Self, rhs: Self) -> Int {
        lhs == rhs ? 0 : (lhs < rhs ? -1 : 1)
    }
}

#if DEBUG
let sample = Money(amount: 12.75, currency: .euro)
let flag: Bool = true && !false
let optional: Int? = nil
let unwrapped = optional ?? 42
#endif
