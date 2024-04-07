/**
* Represents a navigation object with a title and a href.
*/
export class NavObject {
    /**
     * Creates a new NavObject instance.
     * @param title - The title of the navigation object.
     * @param href - The href of the navigation object.
     */
    constructor(public title: string, public href: string) {}

    /**
     * Returns the lowercase version of the title.
     * @returns The lowercase version of the title.
     */
    getLowerCaseTitle(): string {
        return this.title.toLowerCase();
    }
}